from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import mlflow
import mlflow.sklearn
from src.data_processing import load_processed_energy_data

app = FastAPI()

# Load the trained model from MLflow
# Get the latest run from the experiment
experiment = mlflow.get_experiment_by_name("Electricity Forecasting")
runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
latest_run = runs.iloc[0]  # Assuming the first is the latest
run_id = latest_run.run_id
model_uri = f"runs:/{run_id}/model"
model = mlflow.sklearn.load_model(model_uri)

# Load processed data for lags
data = load_processed_energy_data()

class PredictionRequest(BaseModel):
    features: dict

@app.post("/predict")
def predict(request: PredictionRequest):
    features = request.features
    input_df = pd.DataFrame([features])
    prediction = model.predict(input_df)[0]
    return {"prediction": prediction}

@app.get("/data/{date}")
def get_data_for_date(date: str):
    # Parse date and get the row for that date
    target_date = pd.to_datetime(date)
    row = data.loc[data.index.date == target_date.date()]
    if row.empty:
        return {"error": "Date not found in data"}
    # Return the features needed for prediction
    features = row.drop(columns=['value']).iloc[0].to_dict()
    return {"features": features, "actual_value": row['value'].iloc[0]}
