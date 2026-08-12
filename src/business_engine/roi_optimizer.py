import os
import pandas as pd
import xgboost as xgb
import pickle

def calculate_campaign_roi():
    print("Loading data and model for the Business Engine...")
    df = pd.read_csv("data/processed/processed_churn_data.csv")
    
    # Load the exact column names the model expects
    with open("src/models/model_features.pkl", "rb") as f:
        model_features = pickle.load(f)
        
    X = df.drop(columns=['Churn'])
    X = pd.get_dummies(X, drop_first=True)
    X = X[model_features]
    
    # Load your trained XGBoost model
    model = xgb.XGBClassifier()
    model.load_model("src/models/xgboost_churn_model.json")
    
    print("Generating predictions for the customer base...")
    df['Predicted_Churn'] = model.predict(X)
    df['Actual_Churn'] = df['Churn']
    
    # --- The Financial Logic ---
    retention_budget_per_user = 20
    campaign_success_rate = 0.30
    
    print(f"Simulating ROI with a ${retention_budget_per_user} budget per targeted user...")
    
    # Identify who the model says is high risk
    targeted_users = df[df['Predicted_Churn'] == 1].copy()
    total_campaign_cost = len(targeted_users) * retention_budget_per_user
    
    # Calculate financial returns from the ones we successfully save
    true_churners_targeted = targeted_users[targeted_users['Actual_Churn'] == 1]
    saved_customers = int(len(true_churners_targeted) * campaign_success_rate)
    
    # Assume saving them keeps their monthly revenue flowing for 6 more months
    revenue_saved = true_churners_targeted['MonthlyCharges'].mean() * 6 * saved_customers
    net_profit = revenue_saved - total_campaign_cost
    roi_percentage = (net_profit / total_campaign_cost) * 100 if total_campaign_cost > 0 else 0
    
    # --- The Report ---
    report = (
        "\n--- Business Impact & ROI Report ---\n"
        f"Total Customers Analyzed: {len(df)}\n"
        f"High-Risk Users Targeted: {len(targeted_users)}\n"
        f"Total Campaign Cost: ${total_campaign_cost:,.2f}\n"
        f"Estimated Revenue Saved: ${revenue_saved:,.2f}\n"
        f"Net Profit of Campaign: ${net_profit:,.2f}\n"
        f"Campaign ROI: {roi_percentage:.2f}%\n"
    )
    
    print(report)
    
    # Save the report
    os.makedirs("reports", exist_ok=True)
    with open("reports/business_impact.txt", "w") as f:
        f.write(report)
        
    print("Success! Business report saved to reports/business_impact.txt")

if __name__ == "__main__":
    calculate_campaign_roi()