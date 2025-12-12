"""
UAIImputer — Advanced single-file implementation (production-style)
Features:
 - Mixed numeric + categorical handling (scaler + ordinal encoder)
 - Mask-aware encoder (mask concatenated as extra features)
 - VAE-like encoder/decoder with separate numeric mean+var heads and categorical logits head
 - Per-feature gating (learns weight per feature -> blends global vs local imputation)
 - Latent-space neighbor imputation (FAISS optional, CPU fallback)
 - Cluster regularizer (in-batch contrastive-ish term) to improve latent geometry
 - Monte-Carlo sampling for uncertainty (mean + intervals)
 - Sklearn-style API: fit, transform, fit_transform, save, load
 - Persistence for model & preprocessor
 - Configurable hyperparams
"""

import os
import json
import pickle
from typing import Optional, List, Tuple, Union, Dict

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.utils import shuffle as sk_shuffle

import torch
import torch.nn as nn
import torch.nn.functional as F

# Optional FAISS: not required, CPU fallback used if not installed
try:
    import faiss
    FAISS_AVAILABLE = True
except Exception:
    FAISS_AVAILABLE = False

# -----------------------
# Utilities / Preprocessor
# -----------------------

class MixedPreprocessor:
    """
    Handles numeric scaling and categorical ordinal encoding.
    Stores category lists for inverse mapping if needed.
    Transforms DataFrame -> numpy array: [numeric... , cat_ordinal...]
    """
    def __init__(self, numeric_cols: Optional[List[str]] = None, categorical_cols: Optional[List[str]] = None):
        self.numeric_cols = list(numeric_cols) if numeric_cols else []
        self.categorical_cols = list(categorical_cols) if categorical_cols else []
        self.scaler: Optional[StandardScaler] = StandardScaler() if self.numeric_cols else None
        # ordinal encoder uses unknown_value = -1
        self.oencoder: Optional[OrdinalEncoder] = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1) if self.categorical_cols else None
        self.categories_: Dict[str, List[str]] = {}
        self.fitted = False

    def fit(self, df: pd.DataFrame):
        if self.numeric_cols:
            self.scaler.fit(df[self.numeric_cols].astype(float).fillna(0.0))
        if self.categorical_cols:
            tmp = df[self.categorical_cols].astype(object).fillna('##MISSING##')
            self.oencoder.fit(tmp)
            for i, col in enumerate(self.categorical_cols):
                self.categories_[col] = list(self.oencoder.categories_[i])
        self.fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        assert self.fitted, "Preprocessor must be fit before transform"
        parts = []
        if self.numeric_cols:
            num = df[self.numeric_cols].astype(float).fillna(0.0)
            parts.append(self.scaler.transform(num))
        if self.categorical_cols:
            cat = df[self.categorical_cols].astype(object).fillna('##MISSING##')
            parts.append(self.oencoder.transform(cat))
        if parts:
            return np.concatenate(parts, axis=1)
        else:
            return np.zeros((len(df), 0))

    def inverse_transform_numeric(self, arr_numeric: np.ndarray) -> np.ndarray:
        if self.scaler:
            return self.scaler.inverse_transform(arr_numeric)
        return arr_numeric

    def get_splits(self) -> Tuple[int, int]:
        return (len(self.numeric_cols), len(self.categorical_cols))

    def get_categorical_cardinalities(self) -> List[int]:
        return [len(self.categories_[c]) for c in self.categorical_cols] if self.categorical_cols else []

# -----------------------
# Gumbel-softmax utility (categorical sampling)
# -----------------------

def gumbel_softmax_sample(logits: torch.Tensor, tau: float = 1.0, hard: bool = False, eps: float = 1e-20):
    """
    logits: (batch, n_classes)
    returns: one-hot or soft probabilities (batch, n_classes)
    If hard=True, returns differentiable one-hot (straight-through).
    """
    U = torch.rand_like(logits)
    g = -torch.log(-torch.log(U + eps) + eps)
    y = (logits + g) / tau
    y = F.softmax(y, dim=-1)
    if hard:
        y_hard = (y == y.max(dim=-1, keepdim=True)[0]).float()
        y = (y_hard - y).detach() + y
    return y

def sample_categorical_from_logits_all(logits_all: torch.Tensor, categorical_splits: List[int],
                                       tau: float = 0.7, hard: bool = True) -> torch.Tensor:
    """
    logits_all: (batch, sum(cardinalities))
    categorical_splits: list of ints giving sizes of each categorical field
    Returns: tensor (batch, n_cat_fields) with ordinal indices (long)
    """
    outs = []
    idx = 0
    for k in categorical_splits:
        logits_k = logits_all[:, idx: idx + k]
        y = gumbel_softmax_sample(logits_k, tau=tau, hard=hard)  # (batch,k)
        # convert one-hot to index
        idxs = torch.argmax(y, dim=-1).unsqueeze(1)  # (batch,1)
        outs.append(idxs)
        idx += k
    return torch.cat(outs, dim=1)  # (batch, n_cat)

# -----------------------
# Model components
# -----------------------

class Encoder(nn.Module):
    def __init__(self, input_dim: int, hidden_dims: List[int], latent_dim: int, mask_concat: bool = True):
        super().__init__()
        self.input_dim = input_dim + (input_dim if mask_concat else 0)
        layers = []
        prev = self.input_dim
        for h in hidden_dims:
            layers.append(nn.Linear(prev, h))
            layers.append(nn.ReLU(inplace=True))
            prev = h
        self.net = nn.Sequential(*layers)
        self.mu = nn.Linear(prev, latent_dim)
        self.logvar = nn.Linear(prev, latent_dim)

    def forward(self, x: torch.Tensor, mask: torch.Tensor):
        # If mask concat: append mask to x
        xm = torch.cat([x, mask], dim=1)
        h = self.net(xm)
        return self.mu(h), self.logvar(h), h

class Decoder(nn.Module):
    def __init__(self, latent_dim: int, hidden_dims: List[int], numeric_out: int, cat_total_dim: int):
        """
        numeric_out: number of numeric output dims
        cat_total_dim: total logit dims for all categorical fields concatenated
        The decoder will produce:
         - numeric_means: (batch, numeric_out)
         - numeric_logvars: (batch, numeric_out)
         - cat_logits: (batch, cat_total_dim)  (un-normalized scores)
        """
        super().__init__()
        layers = []
        prev = latent_dim
        for h in hidden_dims:
            layers.append(nn.Linear(prev, h))
            layers.append(nn.ReLU(inplace=True))
            prev = h
        self.net = nn.Sequential(*layers)
        self.out_numeric = nn.Linear(prev, numeric_out)
        self.out_num_logvar = nn.Linear(prev, numeric_out)
        self.out_cat_logits = nn.Linear(prev, cat_total_dim) if cat_total_dim > 0 else None

    def forward(self, z: torch.Tensor):
        h = self.net(z)
        num_mu = self.out_numeric(h)
        num_logvar = self.out_num_logvar(h)
        cat_logits = self.out_cat_logits(h) if self.out_cat_logits is not None else None
        return num_mu, num_logvar, cat_logits

class GatingPerFeature(nn.Module):
    """
    Per-feature gating: returns scalar alpha_j in [0,1] per feature j.
    We'll implement as small MLP taking latent mu and outputting vector of size D (num_features)
    """
    def __init__(self, latent_dim: int, out_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, max(64, latent_dim)),
            nn.ReLU(inplace=True),
            nn.Linear(max(64, latent_dim), out_dim),
            nn.Sigmoid()
        )
    def forward(self, z_mu: torch.Tensor):
        return self.net(z_mu)  # shape (batch, out_dim) values in (0,1)

# -----------------------
# Latent Index (FAISS optional)
# -----------------------

class LatentIndexFAISS:
    def __init__(self, dim: int, use_gpu: bool = False):
        if not FAISS_AVAILABLE:
            raise RuntimeError("FAISS not installed")
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.ids = None

    def build(self, latents: np.ndarray, values: np.ndarray):
        # latents: (n, dim) float32, values: (n, d_features) float32
        self.index.reset()
        self.index.add(latents.astype('float32'))
        self.values = values.astype('float32')

    def query(self, q: np.ndarray, k: int = 5):
        D, I = self.index.search(q.astype('float32'), k)
        # gather neighbor values (mean)
        neigh = np.stack([self.values[I[i]] for i in range(I.shape[0])], axis=0)  # (m,k,d)
        return neigh.mean(axis=1)  # (m,d)

class LatentIndexCPU:
    def __init__(self):
        self.latents = None
        self.values = None

    def build(self, latents: np.ndarray, values: np.ndarray):
        self.latents = latents.astype('float32')
        self.values = values.astype('float32')

    def query(self, q: np.ndarray, k: int = 5):
        # naive euclidean distances
        # q: (m, dim)
        dif = self.latents[None, :, :] - q[:, None, :]  # (m, n, dim)
        d2 = (dif ** 2).sum(-1)  # (m, n)
        idx = np.argpartition(d2, k, axis=1)[:, :k]  # (m, k) unsorted
        m = q.shape[0]
        mvals = np.stack([self.values[idx[i]] for i in range(m)], axis=0)  # (m,k,d)
        return mvals.mean(axis=1)  # (m,d)

# -----------------------
# Main UAIImputer class
# -----------------------

class AURAIImputer:
    """
    Advanced Universal Adaptive Imputer (single-file)
    """

    def __init__(self,
                 latent_dim: int = 64,
                 enc_hidden: List[int] = [256, 128],
                 dec_hidden: List[int] = [128, 256],
                 beta: float = 0.1,
                 lambda_cluster: float = 0.01,
                 mc_samples: int = 50,
                 categorical_temperature: float = 0.7,
                 k_neighbors: int = 5,
                 faiss_enabled: bool = False,
                 mask_concat: bool = True,
                 device: Optional[Union[str, torch.device]] = None,
                 verbose: bool = True):
        self.latent_dim = latent_dim
        self.enc_hidden = enc_hidden
        self.dec_hidden = dec_hidden
        self.beta = beta
        self.lambda_cluster = lambda_cluster
        self.mc_samples = mc_samples
        self.cat_temp = categorical_temperature
        self.k_neighbors = k_neighbors
        self.faiss_enabled = faiss_enabled and FAISS_AVAILABLE
        self.mask_concat = mask_concat
        self.device = torch.device(device) if device else (torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'))
        self.verbose = verbose

        # to be set in fit
        self.preprocessor: Optional[MixedPreprocessor] = None
        self.model: Optional[nn.Module] = None
        self.gating: Optional[nn.Module] = None
        self.categorical_splits: List[int] = []
        self.num_numeric = 0
        self.num_categorical = 0
        self.input_dim = 0
        self.latent_index = None  # either Faiss or CPU index
        self._is_fitted = False

    # -----------------------
    # Fit (train) the model on a DataFrame (preferably mostly complete data)
    # -----------------------
    def fit(self,
            df: pd.DataFrame,
            numeric_cols: Optional[List[str]] = None,
            categorical_cols: Optional[List[str]] = None,
            epochs: int = 30,
            batch_size: int = 256,
            lr: float = 1e-3,
            shuffle: bool = True):
        # detect columns if None
        if numeric_cols is None or categorical_cols is None:
            numeric_detect = df.select_dtypes(include=[np.number]).columns.tolist()
            cat_detect = df.select_dtypes(exclude=[np.number]).columns.tolist()
            if numeric_cols is None:
                numeric_cols = numeric_detect
            if categorical_cols is None:
                categorical_cols = cat_detect

        # initialize preprocessor
        self.preprocessor = MixedPreprocessor(numeric_cols=numeric_cols, categorical_cols=categorical_cols)
        self.preprocessor.fit(df)
        X = self.preprocessor.transform(df)  # numpy array (n,d)
        self.num_numeric, self.num_categorical = self.preprocessor.get_splits()
        self.categorical_splits = self.preprocessor.get_categorical_cardinalities()
        self.input_dim = X.shape[1]

        # prepare mask (we assume full data at fit-time; if not, treat NaNs as missing)
        mask = (~np.isnan(X)).astype(float)
        X_filled = X.copy()
        X_filled[mask == 0] = 0.0

        # create model
        # decoder's categorical logits total dim = sum(cardinalities)
        cat_total_dim = sum(self.categorical_splits) if len(self.categorical_splits) > 0 else 0
        # numeric_out is number of numeric dims (we reconstruct numeric dims; categorical logits handled separately)
        numeric_out = self.num_numeric + (sum(self.categorical_splits) if self.num_categorical > 0 else 0)
        # NOTE: numeric_out includes reserved slot space for categorical logits concatenated; decoder outputs unified vector we will split
        self.model = _UAINetwork(self.input_dim, self.latent_dim, enc_hidden=self.enc_hidden, dec_hidden=self.dec_hidden,
                                 num_numeric=self.num_numeric, cat_total_dim=cat_total_dim, mask_concat=self.mask_concat).to(self.device)

        # gating module per-feature (for all features: numeric + categorical encoded columns)
        self.gating = GatingPerFeature(latent_dim=self.latent_dim, out_dim=self.input_dim).to(self.device)

        # train loop
        n = X_filled.shape[0]
        indices = np.arange(n)
        optimizer = torch.optim.Adam(list(self.model.parameters()) + list(self.gating.parameters()), lr=lr)
        # Simple DataLoader logic using numpy slices
        for ep in range(epochs):
            if shuffle:
                indices = sk_shuffle(indices, random_state=ep)
            epoch_loss = 0.0
            count = 0
            for start in range(0, n, batch_size):
                batch_idx = indices[start: start + batch_size]
                xb = torch.tensor(X_filled[batch_idx], dtype=torch.float32, device=self.device)
                mb = torch.tensor(mask[batch_idx], dtype=torch.float32, device=self.device)
                optimizer.zero_grad()
                # forward
                num_mu, num_logvar, cat_logits, mu, logvar = self.model.forward_full(xb, mb)
                # reconstruction loss:
                # numeric NLL (only on observed numeric positions)
                if self.num_numeric > 0:
                    num_obs_mask = mb[:, :self.num_numeric]
                    nll_num = _gaussian_nll(num_mu, num_logvar, xb[:, :self.num_numeric], num_obs_mask)
                else:
                    nll_num = torch.tensor(0.0, device=self.device)
                # categorical cross-entropy on observed categories (if categorical present)
                if self.num_categorical > 0:
                    # observed categorical mask is ones for ordinal-coded columns where original mask==1
                    # Our preprocessor encoded categories into ordinal columns appended after numeric
                    cat_obs_mask = mb[:, self.num_numeric:]  # shape (batch, n_cat_fields)
                    # cat_logits is (batch, sum(cardinalities)) -> split per field
                    # To compute cross-entropy per field we need true ordinal indices from xb
                    true_cat_ordinals = xb[:, self.num_numeric:].long()  # ordinal-encoded (may contain -1 for unknown)
                    # compute CE for each field
                    ce_cat = 0.0
                    start_idx = 0
                    for f_idx, card in enumerate(self.categorical_splits):
                        logits_f = cat_logits[:, start_idx:start_idx + card]  # (batch, card)
                        true_idx = true_cat_ordinals[:, f_idx]  # (batch,)
                        # mask where true_idx >= 0 and field observed
                        valid_mask = (true_idx >= 0) & (cat_obs_mask[:, f_idx] > 0.5)
                        if valid_mask.any():
                            ce = F.cross_entropy(logits_f[valid_mask], true_idx[valid_mask], reduction='mean')
                            ce_cat = ce_cat + ce
                        start_idx += card
                    ce_cat = ce_cat if isinstance(ce_cat, torch.Tensor) else torch.tensor(0.0, device=self.device)
                else:
                    ce_cat = torch.tensor(0.0, device=self.device)

                # KL
                kl = _kl_divergence(mu, logvar)
                # cluster regularizer — encourage compact clusters in latent space across batch
                cluster_reg = mu.var(dim=0).mean()

                # total loss
                loss = nll_num + ce_cat + self.beta * kl + self.lambda_cluster * cluster_reg
                loss.backward()
                torch.nn.utils.clip_grad_norm_(list(self.model.parameters()) + list(self.gating.parameters()), max_norm=5.0)
                optimizer.step()
                epoch_loss += loss.item() * xb.shape[0]
                count += xb.shape[0]
            if self.verbose:
                print(f"[fit] Epoch {ep+1}/{epochs} avg_loss={epoch_loss / max(1,count):.6f}")

            # rebuild latent index each epoch
            self._rebuild_latent_index(X_filled, mask)
        self._is_fitted = True
        return self

    def _rebuild_latent_index(self, X_filled: np.ndarray, mask: np.ndarray):
        # compute latent means for all data
        self.model.eval()
        with torch.no_grad():
            Xt = torch.tensor(X_filled, dtype=torch.float32, device=self.device)
            Mt = torch.tensor(mask, dtype=torch.float32, device=self.device)
            mu_all, _ = self.model.encode_mu_logvar(Xt, Mt)
            mu_np = mu_all.cpu().numpy()
        # values to use for neighbor-based local imputation: raw original arrays X_filled
        values = X_filled.astype('float32')
        if self.faiss_enabled:
            idx = LatentIndexFAISS(dim=mu_np.shape[1])
            idx.build(mu_np, values)
            self.latent_index = idx
        else:
            idx = LatentIndexCPU()
            idx.build(mu_np, values)
            self.latent_index = idx

    # -----------------------
    # Transform / Impute
    # -----------------------
    def transform(self,
                  df_or_array: Union[pd.DataFrame, np.ndarray],
                  mask: Optional[np.ndarray] = None,
                  mc_samples: Optional[int] = None,
                  return_intervals: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
        """
        Impute missing entries.
        df_or_array: DataFrame (will use preprocessor) or numpy array already transformed
        mask: binary mask (1 observed, 0 missing). If None and df_or_array is numpy array with NaNs, mask inferred.
        mc_samples: override default MC sampling
        return_intervals: if True, return (mean, lower, upper)
        """
        assert self._is_fitted, "Call fit() first."
        if isinstance(df_or_array, np.ndarray):
            X = df_or_array.copy()
        else:
            X = self.preprocessor.transform(df_or_array)
        # infer mask
        if mask is None:
            mask = (~np.isnan(X)).astype(float)
        X_obs = X.copy()
        X_obs[mask == 0] = 0.0  # zero-out missing
        mc = mc_samples if mc_samples is not None else self.mc_samples

        model = self.model
        gating = self.gating
        model.eval()
        gating.eval()

        samples = []
        with torch.no_grad():
            Xt = torch.tensor(X_obs, dtype=torch.float32, device=self.device)
            Mt = torch.tensor(mask, dtype=torch.float32, device=self.device)
            mu, logvar = model.encode_mu_logvar(Xt, Mt)  # (n, latent)
            for t in range(mc):
                # sample z
                std = (0.5 * logvar).exp()
                z = mu + torch.randn_like(std) * std
                # decode
                num_mu, num_logvar, cat_logits = model.decode_from_z(z)
                # construct full recon vector (numeric means + concatenated cat sampled as ordinal indices)
                # For categorical, sample via gumbel-softmax (hard)
                if self.num_categorical > 0:
                    # sample categories per-field
                    cat_sample_idxs = sample_categorical_from_logits_all(cat_logits, self.categorical_splits, tau=self.cat_temp, hard=True)
                    # cat_sample_idxs: (n, n_cat_fields) ordinal indices
                    cat_sample_idxs_float = cat_sample_idxs.float()
                    recon_numeric = torch.cat([num_mu, cat_sample_idxs_float], dim=1)
                else:
                    recon_numeric = num_mu

                # local neighbor impute: query index with mu.cpu().numpy()
                try:
                    local_vals = self.latent_index.query(mu.cpu().numpy(), k=self.k_neighbors)
                    local_vals = torch.tensor(local_vals, dtype=torch.float32, device=self.device)
                except Exception:
                    # fallback to recon_numeric as local
                    local_vals = recon_numeric

                # gating per-feature (alpha_j between 0..1)
                alpha = gating(mu)  # (n, input_dim)
                # ensure alpha shape matches
                if alpha.shape[1] != recon_numeric.shape[1]:
                    # if gating outputs different dims (shouldn't), broadcast scalar
                    alpha = alpha.mean(dim=1, keepdim=True).repeat(1, recon_numeric.shape[1])

                gated = alpha * recon_numeric + (1.0 - alpha) * local_vals
                filled = Xt * Mt + gated * (1.0 - Mt)
                samples.append(filled.cpu().numpy())

        arr = np.stack(samples, axis=0)  # (mc, n, d)
        mean_imp = arr.mean(axis=0)
        if return_intervals:
            lower = np.percentile(arr, 2.5, axis=0)
            upper = np.percentile(arr, 97.5, axis=0)
            return mean_imp, lower, upper
        return mean_imp

    # -----------------------
    # Persistence
    # -----------------------
    def save(self, path: str):
        os.makedirs(path, exist_ok=True)
        # save model state dict and gating
        torch.save(self.model.state_dict(), os.path.join(path, "model.pth"))
        torch.save(self.gating.state_dict(), os.path.join(path, "gating.pth"))
        # save metadata & preprocessor
        meta = {
            "latent_dim": self.latent_dim,
            "enc_hidden": self.enc_hidden,
            "dec_hidden": self.dec_hidden,
            "beta": self.beta,
            "lambda_cluster": self.lambda_cluster,
            "mc_samples": self.mc_samples,
            "cat_temp": self.cat_temp,
            "k_neighbors": self.k_neighbors,
            "faiss_enabled": self.faiss_enabled,
            "mask_concat": self.mask_concat,
            "num_numeric": self.num_numeric,
            "num_categorical": self.num_categorical,
            "categorical_splits": self.categorical_splits,
            "input_dim": self.input_dim
        }
        with open(os.path.join(path, "meta.json"), "w") as f:
            json.dump(meta, f)
        # preprocessor via pickle
        with open(os.path.join(path, "preprocessor.pkl"), "wb") as f:
            pickle.dump(self.preprocessor, f)
        return path

    @classmethod
    def load(cls, path: str, device: Optional[Union[str, torch.device]] = None):
        with open(os.path.join(path, "meta.json"), "r") as f:
            meta = json.load(f)
        obj = cls(latent_dim=meta.get("latent_dim", 64),
                  enc_hidden=meta.get("enc_hidden", [256,128]),
                  dec_hidden=meta.get("dec_hidden", [128,256]),
                  beta=meta.get("beta", 0.1),
                  lambda_cluster=meta.get("lambda_cluster", 0.01),
                  mc_samples=meta.get("mc_samples", 50),
                  categorical_temperature=meta.get("cat_temp", 0.7),
                  k_neighbors=meta.get("k_neighbors", 5),
                  faiss_enabled=meta.get("faiss_enabled", False),
                  mask_concat=meta.get("mask_concat", True),
                  device=device)
        # load preprocessor
        with open(os.path.join(path, "preprocessor.pkl"), "rb") as f:
            obj.preprocessor = pickle.load(f)
        obj.num_numeric = meta.get("num_numeric", 0)
        obj.num_categorical = meta.get("num_categorical", 0)
        obj.categorical_splits = meta.get("categorical_splits", [])
        obj.input_dim = meta.get("input_dim", 0)

        # recreate model and gating, load weights
        cat_total_dim = sum(obj.categorical_splits) if obj.categorical_splits else 0
        obj.model = _UAINetwork(obj.input_dim, obj.latent_dim, enc_hidden=obj.enc_hidden, dec_hidden=obj.dec_hidden,
                                num_numeric=obj.num_numeric, cat_total_dim=cat_total_dim, mask_concat=obj.mask_concat).to(obj.device)
        obj.gating = GatingPerFeature(latent_dim=obj.latent_dim, out_dim=obj.input_dim).to(obj.device)
        obj.model.load_state_dict(torch.load(os.path.join(path, "model.pth"), map_location=obj.device))
        obj.gating.load_state_dict(torch.load(os.path.join(path, "gating.pth"), map_location=obj.device))
        obj._is_fitted = True
        return obj

# -----------------------
# Internal helper network wrapper
# -----------------------

class _UAINetwork(nn.Module):
    """
    Wraps encoder and decoder. Exposes:
     - forward_full(x, mask) -> num_mu, num_logvar, cat_logits, mu, logvar
     - encode_mu_logvar(x, mask) -> mu, logvar
     - decode_from_z(z) -> num_mu, num_logvar, cat_logits
    """
    def __init__(self, input_dim: int, latent_dim: int, enc_hidden: List[int], dec_hidden: List[int],
                 num_numeric: int, cat_total_dim: int, mask_concat: bool = True):
        super().__init__()
        self.encoder = Encoder(input_dim, hidden_dims=enc_hidden, latent_dim=latent_dim, mask_concat=mask_concat)
        self.decoder = Decoder(latent_dim, hidden_dims=dec_hidden, numeric_out=num_numeric, cat_total_dim=cat_total_dim)

    def forward_full(self, x: torch.Tensor, mask: torch.Tensor):
        mu, logvar, _ = self.encoder(x, mask)
        std = (0.5 * logvar).exp()
        eps = torch.randn_like(std)
        z = mu + eps * std
        num_mu, num_logvar, cat_logits = self.decoder(z)
        return num_mu, num_logvar, cat_logits, mu, logvar

    def encode_mu_logvar(self, x: torch.Tensor, mask: torch.Tensor):
        mu, logvar, _ = self.encoder(x, mask)
        return mu, logvar

    def decode_from_z(self, z: torch.Tensor):
        return self.decoder(z)

# -----------------------
# Loss helpers
# -----------------------

def _gaussian_nll(mu_pred: torch.Tensor, logvar_pred: torch.Tensor, x_true: torch.Tensor, mask: torch.Tensor):
    var = torch.exp(logvar_pred).clamp(min=1e-6)
    se = (x_true - mu_pred) ** 2
    nll = 0.5 * (torch.log(2 * np.pi * var) + se / var)
    denom = mask.sum().clamp(min=1.0)
    return (nll * mask).sum() / denom

def _kl_divergence(mu: torch.Tensor, logvar: torch.Tensor):
    return -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp()) / mu.size(0)
