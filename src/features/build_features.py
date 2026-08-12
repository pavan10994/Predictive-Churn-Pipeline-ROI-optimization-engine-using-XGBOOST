import os
import pandas as pd
import numpy as np

def clean_and_engineer_features(
    input_path="data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv", 
    output_path="data/processed/processed_churn_data.csv"
):
    print("Loading validated raw data...")
    df = pd.read_csv(input_path)
    
    print("Cleaning data...")
    # 1. TotalCharges contains hidden blank spaces " " instead of standard null values. 
    # We force them to NaN, then fill with 0 (since tenure is 0 for these specific new users).
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].replace(" ", ""), errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
    
    # 2. Convert the target variable 'Churn' to binary integers (1 and 0) for XGBoost
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    
    # 3. Drop CustomerID as it provides no mathematical predictive value
    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])
        
    print("Engineering business features...")
    # 4. Create a new feature to help segment customers for the business engine
    df['TenureYears'] = df['tenure'] / 12.0
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Saving processed data to {output_path}...")
    df.to_csv(output_path, index=False)
    print("Feature engineering complete!")

if __name__ == "__main__":
    clean_and_engineer_features()