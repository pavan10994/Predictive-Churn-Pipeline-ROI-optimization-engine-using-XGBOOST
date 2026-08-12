import streamlit as st
import requests

# Configure the visual layout of the page
st.set_page_config(page_title="Churn & ROI Dashboard", layout="centered")

st.title("📊 Telco Churn & ROI Predictor")
st.markdown("Predict customer churn risk and simulate the financial ROI of targeted retention campaigns.")

st.divider()

# Create the user input form
with st.form("customer_data"):
    st.subheader("Customer Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        tenure = st.number_input("Tenure (Months)", min_value=0, max_value=100, value=12)
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=75.0)
        total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=900.0)
        
    with col2:
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])

    submit = st.form_submit_button("Predict Risk & ROI")

# When the user clicks the button...
if submit:
    # 1. Package the data just like our API expects
    customer_data = {
        "tenure": tenure,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "Contract": contract,
        "InternetService": internet,
        "PaymentMethod": payment
    }
    
    try:
        # 2. Send the data to our FastAPI server
        with st.spinner("Analyzing risk profile..."):
            api_url = "https://predictive-churn-pipeline-roi-d9w9.onrender.com/predict"
            response = requests.post(api_url, json=customer_data)
            result = response.json()
            
        # 3. Display the Business Results
        st.divider()
        st.subheader("🤖 AI Engine Results")
        
        risk_col, roi_col = st.columns(2)
        
        with risk_col:
            if result["high_risk_flag"]:
                st.error(f"**High Churn Risk:** {result['risk_percentage']}")
            else:
                st.success(f"**Low Churn Risk:** {result['risk_percentage']}")
                
        with roi_col:
            # Calculate a quick ROI estimate for the dashboard
            if result["high_risk_flag"]:
                clv_saved = monthly_charges * 6  # Assume saving them retains 6 months of revenue
                campaign_cost = 20.0
                net_profit = clv_saved - campaign_cost
                roi = (net_profit / campaign_cost) * 100
                st.metric(label="Campaign ROI (vs $20 Cost)", value=f"{roi:.0f}%", delta=f"+${net_profit:,.2f} Profit")
            else:
                st.metric(label="Action Recommendation", value="No intervention needed")
                
    except Exception as e:
        st.error(f"⚠️ Code Error: {e}")
        if 'response' in locals():
            st.write("Server actually said:", response.text)