import os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
import pickle

def train_model(data_path="data/processed/processed_churn_data.csv", model_dir="src/models"):
    print("Loading processed data...")
    df = pd.read_csv(data_path)
    
    y = df['Churn']
    X = df.drop(columns=['Churn'])
    
    print("Encoding text categories into numbers...")
    X = pd.get_dummies(X, drop_first=True)
    
    print("Splitting data into 80% training and 20% testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Calculate the exact imbalance ratio dynamically
    # (Number of Negative class instances / Number of Positive class instances)
    imbalance_ratio = len(y_train[y_train == 0]) / len(y_train[y_train == 1])
    
    print(f"Applying class balancing weight: {imbalance_ratio:.2f}")
    print("Training the XGBoost model...")
    model = xgb.XGBClassifier(
        n_estimators=100, 
        learning_rate=0.1, 
        max_depth=5, 
        scale_pos_weight=imbalance_ratio,  # <-- The efficiency upgrade
        random_state=42
    )
    model.fit(X_train, y_train)
    
    print("Evaluating model performance...")
    y_pred_prob = model.predict_proba(X_test)[:, 1]
    y_pred = model.predict(X_test)
    
    auc = roc_auc_score(y_test, y_pred_prob)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n--- Model Results ---")
    print(f"AUC-ROC Score: {auc:.4f}")
    print(f"Accuracy: {accuracy:.4f}\n")
    print(classification_report(y_test, y_pred))
    
    print("Saving the trained model...")
    os.makedirs(model_dir, exist_ok=True)
    model.save_model(os.path.join(model_dir, "xgboost_churn_model.json"))
    
    with open(os.path.join(model_dir, "model_features.pkl"), "wb") as f:
        pickle.dump(list(X.columns), f)
        
    print("Success! Model training complete and saved.")

if __name__ == "__main__":
    train_model()