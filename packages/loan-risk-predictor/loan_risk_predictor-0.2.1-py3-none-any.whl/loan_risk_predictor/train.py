from loan_risk_predictor.data_preprocessing import load_data, preprocess_data
from loan_risk_predictor.model import train_model

def main():
    """Main function to run the training pipeline."""
    print("Loading data...")
    df = load_data()
    
    print("Preprocessing data...")
    X_scaled, y, _, _ = preprocess_data(df)
    
    print("Training model...")
    model = train_model(X_scaled, y)
    
    print("Training complete.")

if __name__ == "__main__":
    main()