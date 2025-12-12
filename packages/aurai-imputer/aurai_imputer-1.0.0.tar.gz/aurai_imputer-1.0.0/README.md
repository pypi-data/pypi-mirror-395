# UAI – Universal Adaptive Imputer
**Author:** Abdul Mofique Siddiqui  
**License:** MIT  
**Install via pip:**
```bash
pip install UAI
```
Import it in your Python code:
```python
from UAI import UAIImputer
```

## Overview
UAI (Universal Adaptive Imputer) is a hybrid imputation framework that combines a Variational Autoencoder, latent-space nearest-neighbor search, and a feature-wise adaptive gating mechanism. It is designed to handle missing data in both numerical and categorical datasets and performs effectively under MCAR, MAR, and MNAR missingness patterns.

UAI also provides uncertainty estimates for each imputed value via Monte Carlo sampling, making it suitable for tasks that require high reliability.

## Installation
Install the package via pip:
```bash
pip install uai
```

## How It Works
- **Global VAE Module**: Learns latent representations and reconstructs numerical and categorical features.
- **Latent KNN Module**: Performs local neighbor aggregation in latent space for fine-grained imputation.
- **Adaptive Gating**: Learns a per-feature weight to combine global and local predictions.
- **Uncertainty Estimation**: Monte Carlo sampling provides predictive mean and confidence intervals.
- **Mixed Data Support**: Handles both numerical and categorical data through scaling and ordinal encoding.

## Getting Started

### 1. Import the package
```python
from UAI import UAIImputer
```

### 2. Initialize the imputer
```python
imputer = UAIImputer()
```

### 3. Fit the model
```python
imputer.fit(df)
```
- `df`: pandas DataFrame containing numerical and/or categorical columns

### 4. Impute missing values
```python
imputed = imputer.transform(df)
```
Returns a numpy array with missing values filled

### 5. Impute with uncertainty intervals
```python
mean, lower, upper = imputer.transform(df, return_intervals=True)
```
Returns the imputed mean as well as 95% confidence bounds

## API Reference

### UAIImputer()
Initializes the imputer. Supports optional parameters such as latent dimension, Monte Carlo samples, and number of neighbors.

### .fit(df)
Fits the model to the training data.

**Parameters:**
- `df`: pandas DataFrame with mixed (numeric + categorical) features

### .transform(df, return_intervals=False)
Returns imputed values.

**Input:**
- `df`: DataFrame or numpy array with missing values

**Output:**
- Imputed numpy array
- If `return_intervals=True`: returns `(mean, lower, upper)` arrays

### .save(path)
Saves the trained imputer (model weights, preprocessor, metadata).

### .load(path)
Loads a previously saved UAI model from disk.

## Example Usage

### Example 1: Basic Imputation
```python
from UAI import UAIImputer
import pandas as pd

df = pd.read_csv("data.csv")
imputer = UAIImputer()
imputer.fit(df)
imputed = imputer.transform(df)
```

### Example 2: Imputation with Uncertainty
```python
mean, lower, upper = imputer.transform(df, return_intervals=True)
```

## Internals
- **Variational Autoencoder**: Learns global structure and reconstructs numeric means, variances, and categorical logits.
- **Latent-Space KNN**: Aggregates neighbor values to capture local structure.
- **Gating Network**: Outputs per-feature blending weights to combine global and local predictions.
- **Cluster Regularization**: Encourages stable latent geometry.
- **Monte Carlo Sampling**: Produces confidence intervals for each imputed feature.

## Notes
- Supports both numerical and categorical data.
- Performs reliably under MCAR, MAR, and MNAR missingness.
- Uncertainty intervals can assist downstream decision-making.
- GPU recommended for faster training.

## Author
Abdul Mofique Siddiqui

## License
This project is licensed under the MIT License.