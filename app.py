import streamlit as st
import pandas as pd
import joblib


model = joblib.load("churn_model.pkl")
scaler = joblib.load("scaler.pkl")
training_columns = joblib.load("training_columns.pkl")

def explain_churn(probability):
 if probability > 0.60:
        return f""" 🔴 High Churn Risk 
        This customer is very likely to leave.
        Recommended Action:
        rovide discounts, loyalty offers, or upgrade plans."""
 elif probability > 0.30:
        return f""" 🟡 Medium Churn Risk
        This customer may churn in the future.
        Recommended Action:
        Improve engagement and monitor activity."""
 else:
        return f""" 🟢 Low Churn Risk 
        This customer is stable.
        Recommended Action:
        Maintain current services quality."""
    

st.title("Customer Churn Prediction App")
tenure = st.number_input("Tenure (months)",min_value=0,value=12)
monthly_charges = st.number_input("Monthly Charges", min_value=0.0,value=70.0)
total_charges = st.number_input("Total Charges",min_value =0.0,value=1000.0)
senior_citizen = st.selectbox("Senior Citizen",[0,1])
contract = st.selectbox("Contract Type",["Month-to-month","One Year","Two Year"])
payment_method = st.selectbox("Payment Method",["Electronic check","Mailed check","Bank transfer(automatic)","Credit card(automatic)"])

input_df = pd.DataFrame({"tenure":[tenure],"MonthlyCharges":[monthly_charges],
 "TotalCharges":[total_charges],"SeniorCitizen": [senior_citizen]
 ,"Contract":[contract],"PaymentMethod":[payment_method]})

input_df=pd.get_dummies(input_df,drop_first=True)
input_df=input_df.reindex(columns=training_columns,fill_value=0)

num_cols = list(scaler.feature_names_in_)
input_df[num_cols]=scaler.transform(input_df[num_cols])

if st.button("Predict Churn"):
    with st.spinner("Predicting ..."):
         churn_prob= model.predict_proba(input_df)[0][1]

    st.write(f"📉Churn Probability : {churn_prob*100:.2f}%")
     
    if churn_prob > 0.60 :
        st.error("🔴 High Risk of Churn")
        st.write("Action: Offer discounts, call customer immediately, provide retention benefits.")
    elif churn_prob > 0.30:
        st.warning("🟡 Medium Risk of Churn")
        st.write("Action: Improve engagement, send offers, monitor behavior.")
    else:
        st.success("🟢 Low Risk of Churn")
        st.write("Action: Upsell premium plans and loyalty programs")
    
    explanation = explain_churn(churn_prob)
    st.write("### Explanation:")
    st.write(explanation)
    st.subheader("Top Factors Influencing Prediction")
    importance = model.feature_importances_
    df_imp = pd.DataFrame({
         "Feature" : training_columns,
         "Importance": importance
         }).sort_values(by="Importance",ascending=False).head(10)
    st.bar_chart(df_imp.set_index("Feature"))
    