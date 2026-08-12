import pandas as pd
import pandera as pa
from pandera.typing import Series

class TelcoSchema(pa.DataFrameModel):
    """
    The blueprint for our raw data. If the Kaggle data doesn't 
    match this exactly, the pipeline stops.
    """
    customerID: Series[str]
    gender: Series[str] = pa.Field(isin=["Male", "Female"])
    SeniorCitizen: Series[int] = pa.Field(isin=[0, 1])
    
    # Tenure and MonthlyCharges cannot be negative
    tenure: Series[int] = pa.Field(ge=0)
    MonthlyCharges: Series[float] = pa.Field(ge=0)
    
    # TotalCharges has hidden blank spaces in the raw data, so we check it as a string for now
    TotalCharges: Series[str] 
    
    Churn: Series[str] = pa.Field(isin=["Yes", "No"])

def validate_raw_data(file_path: str = "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"):
    print("Loading raw data for validation...")
    df = pd.read_csv(file_path)
    
    print("Checking data against the rules...")
    try:
        # This checks the data against our blueprint
        TelcoSchema.validate(df)
        print("Success! Data is clean and passed all checks.")
    except Exception as e:
        print(f"Validation Failed! Bad data found: {e}")
        raise

if __name__ == "__main__":
    validate_raw_data()