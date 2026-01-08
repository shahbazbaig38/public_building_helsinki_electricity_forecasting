import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import subprocess

# FastAPI base URL
API_BASE_URL = "http://localhost:8000"

st.title("Electricity Forecasting App")

# Section for predictions
st.header("Make a Prediction")
st.write("Select a date from 2024 to get real features and predict electricity consumption.")

# Date picker for 2024
selected_date = st.date_input("Select Date (2024)", value=datetime(2024, 1, 1), min_value=datetime(2024, 1, 1), max_value=datetime(2024, 12, 31))

if st.button("Fetch Features and Predict"):
    date_str = selected_date.strftime("%Y-%m-%d")
    try:
        # Fetch features for the selected date
        response = requests.get(f"{API_BASE_URL}/data/{date_str}")
        if response.status_code == 200:
            data = response.json()
            features = data["features"]
            actual_value = data["actual_value"]
            st.write("Fetched Features:")
            st.json(features)
            st.write(f"Actual Value: {actual_value}")

            # Now predict using these features
            pred_response = requests.post(f"{API_BASE_URL}/predict", json={"features": features})
            if pred_response.status_code == 200:
                prediction = pred_response.json()["prediction"]
                st.success(f"Predicted Electricity Consumption: {prediction}")
                st.write(f"Actual vs Predicted: {actual_value} vs {prediction}")
            else:
                st.error("Error in prediction")
        else:
            st.error("Date not found in data")
    except Exception as e:
        st.error(f"Failed to connect to API: {e}")

# Section for evaluation
st.header("Model Evaluation")
if st.button("Run Evaluation"):
    try:
        # Run the evaluation script
        result = subprocess.run(["python", "src/evaluation.py"], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("Evaluation completed successfully.")
            st.text(result.stdout)
        else:
            st.error("Evaluation failed.")
            st.text(result.stderr)
    except Exception as e:
        st.error(f"Error running evaluation: {e}")
