# Loan Risk Predictor

[![PyPI version](https://img.shields.io/pypi/v/loan-risk-predictor)](https://pypi.org/project/loan-risk-predictor/)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/shanujans/loan-risk-prediction/publish-to-pypi.yml)](https://github.com/shanujans/loan-risk-prediction/actions)
[![PyPI - License](https://img.shields.io/pypi/l/loan-risk-predictor)](https://github.com/shanujans/loan-risk-prediction/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/loan-risk-predictor)](https://pypi.org/project/loan-risk-predictor/)

A complete Python package to predict loan default risk using a Decision Tree model. This project is built from a Kaggle notebook and has been structured as a robust, installable package published on PyPI.

## Overview

This project provides a full pipeline for a machine learning task, including data loading, preprocessing, model training, and evaluation. It is designed to be both a ready-to-use tool and a clear example of how to convert a data science notebook into a distributable software package following modern best practices like `src`-layout and `pyproject.toml` configuration.

## Key Features

-   **Data Preprocessing**: Handles missing values, encodes categorical features, and scales numerical data.
-   **Model Training**: Implements a `DecisionTreeClassifier` from scikit-learn.
-   **Packaged for Distribution**: Published on PyPI and installable with a single `pip` command.
-   **Modular Code**: Logic is separated into modules for data handling and model training.
-   **Command-Line & Library Usage**: Can be run directly from the terminal or imported into other Python projects.

## Technology Stack

-   **Python 3.7+**
-   **Pandas**: For data manipulation and loading.
-   **Scikit-learn**: For data preprocessing and machine learning modeling.
-   **Numpy**: For numerical operations.
-   **Setuptools & Build**: For packaging and distribution.
-   **GitHub Actions**: For Continuous Integration and automated publishing to PyPI.

## Installation

You can install the Loan Risk Predictor directly from PyPI:

```bash
pip install loan-risk-predictor
```

## Usage

There are two primary ways to use this package.

#### 1. As a Command-Line Tool

The simplest way to run the full training pipeline is to execute the package as a Python module. This will load the included dataset, preprocess it, train the model, and print the evaluation results.

```bash
python -m loan_risk_predictor.train
```

You should see an output like this:
```
Loading data...
Preprocessing data...
Training model...
Model Accuracy: 0.8754
Classification Report:
              precision    recall  f1-score   support
           0       0.88      0.99      0.93     44123
           1       0.49      0.08      0.14      6277
    accuracy                           0.88     50400
   macro avg       0.68      0.54      0.53     50400
weighted avg       0.83      0.88      0.83     50400
Training complete.
```

#### 2. As a Python Library

For more advanced use, you can import the functions directly into your own scripts or notebooks. This allows you to integrate the components into a custom workflow.

Here is an example:

```python
# main_script.py
from loan_risk_predictor.data_preprocessing import load_data, preprocess_data
from loan_risk_predictor.model import train_model

def run_custom_pipeline():
    """
    An example of how to use the library functions programmatically.
    """
    print("--- Starting Custom Pipeline ---")
    
    # 1. Load the data
    print("Step 1: Loading data...")
    raw_df = load_data()
    print(f"Loaded dataset with {raw_df.shape} rows.")
    
    # 2. Preprocess the data
    print("\nStep 2: Preprocessing data...")
    X_scaled, y, scaler, encoders = preprocess_data(raw_df)
    print("Data has been cleaned, encoded, and scaled.")
    
    # 3. Train the model
    print("\nStep 3: Training the model...")
    trained_model = train_model(X_scaled, y)
    print("Model training is complete.")
    
    print("\n--- Custom Pipeline Finished ---")
    # You can now use the `trained_model` object for predictions,
    # or the `scaler` and `encoders` for new data.

if __name__ == "__main__":
    run_custom_pipeline()```
```
## Project Structure

This project follows the modern `src`-layout to ensure a clean and robust package structure.

```text
loan-risk-predictor/
├── src/
│   └── loan_risk_predictor/      # Main package source
│       ├── data/
│       │   └── training.csv      # Packaged data
│       ├── data_preprocessing.py
│       ├── model.py
│       └── train.py
│
├── .github/
│   └── workflows/
│       └── publish-to-pypi.yml   # CI/CD workflow
│
├── notebooks/
│   └── exploration.ipynb         # Original exploratory notebook
│
├── .gitignore
├── LICENSE
├── pyproject.toml                # Main packaging configuration
└── README.md
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to fix a bug, please follow these steps:

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally: `git clone https://github.com/shanujans/loan-risk-prediction.git`
3.  **Create a new branch** for your feature: `git checkout -b feature/loan-risk-prediction`
4.  **Install dependencies** in a virtual environment.
5.  **Make your changes** and commit them with a clear message.
6.  **Push your branch** to your fork: `git push origin feature/loan-risk-prediction`
7.  **Create a Pull Request** from your fork to the original repository.

## Roadmap

Future improvements could include:

-   [ ] **Trying different models** (e.g., RandomForest, Gradient Boosting) for comparison.
-   [ ] **Adding hyperparameter tuning** using GridSearchCV or RandomizedSearchCV.
-   [ ] **Implementing a prediction script** to score new, unseen data.
-   [ ] **Adding a comprehensive test suite** with `pytest`.
-   [ ] **Containerizing the application** with Docker.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
