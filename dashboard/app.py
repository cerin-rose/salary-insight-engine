import streamlit as st
import pandas as pd
import joblib

st.title("💼 Salary Insight Engine")
model = joblib.load("models/salary_predictor.pkl")

job = st.text_input("Job Title", "Software Developer")
company = st.text_input("Company", "Amazon")
location = st.text_input("Location", "United States")
experience = st.number_input("Experience (Years)", min_value=0, max_value=50, value=3)

if st.button("Predict Salary"):
    X = pd.DataFrame([{
        "job_title": job,
        "company": company,
        "location": location,
        "experience": experience
    }])
    pred = model.predict(X)[0]
    st.success(f"💰 Estimated Salary: ${pred:,.2f}")
