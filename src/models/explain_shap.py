import os
import pandas as pd
import xgboost as xgb
import shap
import matplotlib.pyplot as plt
import pickle

def generate_shap_explanations(
    data_path="data/processed/processed_churn_data.csv",
    model_path="src/models/xgboost_churn_model.json",
    features_path="src/models/model_features.pkl",
    output_dir="reports" # We will save the chart here
):
    print("Loading data and model for SHAP analysis...")
    df = pd.read_csv(data_path)
    
    # Load the exact column names the model expects
    with open(features_path, "rb") as f:
        model_features = pickle.load(f)
        
    X = df.drop(columns=['Churn'])
    X = pd.get_dummies(X, drop_first=True)
    
    # Ensure our data exactly matches the model's training columns
    X = X[model_features]
    
    # Load the trained XGBoost model
    model = xgb.XGBClassifier()
    model.load_model(model_path)
    
    print("Calculating SHAP values (this may take a few seconds)...")
    explainer = shap.TreeExplainer(model)
    
    # To keep the pipeline fast, we explain a random sample of 1000 customers
    X_sample = X.sample(n=1000, random_state=42)
    shap_values = explainer.shap_values(X_sample)
    
    print("Generating SHAP summary plot...")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create and format the plot
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_sample, show=False)
    plt.tight_layout()
    
    # Save the plot
    plot_path = os.path.join(output_dir, "shap_summary.png")
    plt.savefig(plot_path)
    plt.close()
    
    print(f"Success! SHAP summary plot saved to {plot_path}")

if __name__ == "__main__":
    generate_shap_explanations()