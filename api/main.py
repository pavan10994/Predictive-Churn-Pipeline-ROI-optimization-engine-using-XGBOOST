from fastapi import FastAPI
import pandas as pd
import xgboost as xgb
import pickle

# Create the API application
app = FastAPI(title="Telco Churn Prediction API", version="1.0")

# Load the model and features into memory when the server starts
model = xgb.XGBClassifier()
model.load_model("src/models/xgboost_churn_model.json")

with open("src/models/model_features.pkl", "rb") as f:
    model_features = pickle.load(f)

@app.post("/predict")
def predict_churn(customer_data: dict):
    """
    Receives raw customer data, processes it, and returns the churn probability.
    """
    # 1. Convert incoming JSON to a pandas DataFrame
    df = pd.DataFrame([customer_data])
    
    # 2. Re-create the engineered features we built during training
    if 'tenure' in df.columns:
        df['TenureYears'] = df['tenure'] / 12.0
        
    # 3. Convert text to numbers (Dummy Encoding)
    df = pd.get_dummies(df, drop_first=True)
    
    # 4. Ensure the API data perfectly matches the model's training data
    # (If a category is missing from this single customer, fill it with 0)
    for col in model_features:
        if col not in df.columns:
            df[col] = 0
            
    # Order the columns exactly as the model expects
    X = df[model_features]
    
    # 5. Make the prediction!
    churn_prob = model.predict_proba(X)[0][1]
    is_high_risk = int(model.predict(X)[0])
    
    # Return the results to the user/website
    return {
        "churn_probability": float(churn_prob),
        "risk_percentage": f"{churn_prob * 100:.2f}%",
        "high_risk_flag": bool(is_high_risk == 1)
    }