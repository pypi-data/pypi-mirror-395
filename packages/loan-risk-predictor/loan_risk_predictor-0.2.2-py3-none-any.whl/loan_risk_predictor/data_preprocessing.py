import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from importlib import resources

def load_data():
    """Loads the training data from the package resources."""
    with resources.path("loan_risk_predictor.data", "training.csv") as data_path:
        return pd.read_csv(data_path)

def preprocess_data(df):
    """Cleans, encodes, and scales the loan risk dataset."""
    # Drop unnecessary columns if any (Id is often dropped)
    df = df.drop(columns=['Id'], errors='ignore')
    
    # Handle missing values (simple fillna for this example)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna(df[col].mode()[0])
    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].fillna(df[col].median())

    # Encode categorical features
    label_encoders = {}
    for column in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le
        
    # Separate features and target
    X = df.drop('Risk_Flag', axis=1)
    y = df['Risk_Flag']
    
    # Scale numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y, scaler, label_encoders