# Loan Risk Predictor

A Python package to predict loan default risk based on applicant data. This project is built from a Kaggle notebook and structured as an installable PyPI package.

## Features

- Data preprocessing including cleaning, encoding, and scaling.
- A Decision Tree classification model for risk prediction.
- A simple pipeline to load data and train the model.

## Installation

You will be able to install this package from PyPI:

```bash
pip install loan-risk-predictor
```

### How to Use

After installation, you can run the training pipeline directly from the command line:

```bash
python -m loan_risk_model.train
```
### Project Structure

loan-risk-predictor/
│
├── loan_risk_model/
│   ├── data/
│   │   └── training.csv
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── model.py
│   └── train.py
│
├── notebooks/
│   └── Your-Kaggle-Notebook.ipynb
│
└── ... (packaging files)
