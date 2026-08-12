import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="Telco Churn & ROI Predictor", layout="centered")

st.title("📊 Telco Churn & ROI Predictor")
st.write("Enter customer details below to predict churn risk and simulate campaign ROI.")

# Input Form
with st.form("churn_form"):
    st.subheader("Customer Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tenure = st.number_input("Tenure (Months)", min_value=0, max_value=100, value=12)
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=75.0)
        total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=900.0)
        
    with col2:
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        payment = st.selectbox("Payment Method", [
            "Electronic check", 
            "Mailed check", 
            "Bank transfer (automatic)", 
            "Credit card (automatic)"
        ])

    submit = st.form_submit_button("Predict Churn Risk")

# Prediction Execution
if submit:
    # 1. Payload
    customer_data = {
        "tenure": tenure,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "Contract": contract,
        "InternetService": internet,
        "PaymentMethod": payment
    }

    # 2. Live API URL (Replace with your actual Render URL)
    api_url = "https://predictive-churn-pipeline-roi-d9w9.onrender.com/predict"

    try:
        with st.spinner("Analyzing risk profile..."):
            response = requests.post(api_url, json=customer_data, timeout=10)

        if response.status_code == 200:
            result = response.json()
            
            st.divider()
            st.subheader("Analysis Results")
            
            # Show Risk Level
            if result.get("high_risk_flag"):
                st.error(f"**High Churn Risk Detected:** {result.get('risk_percentage')}")
                
                # Simple Campaign ROI Math
                clv_saved = monthly_charges * 6
                campaign_cost = 20.0
                net_profit = clv_saved - campaign_cost
                roi = (net_profit / campaign_cost) * 100
                
                res_col1, res_col2 = st.columns(2)
                res_col1.metric(label="Potential CLV Saved (6 Mo)", value=f"${clv_saved:,.2f}")
                res_col2.metric(label="Campaign ROI", value=f"{roi:.0f}%", delta=f"+${net_profit:,.2f} Profit")
            else:
                st.success(f"**Low Churn Risk:** {result.get('risk_percentage')}")
                st.info("Action Recommendation: No retention intervention required.")
        else:
            st.error(f"API Error ({response.status_code}): {response.text}")

    except Exception as e:
        st.error(f"Connection Failed: {e}")