import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
from data_processing import load_processed_energy_data

# Load processed data
data = load_processed_energy_data()

# Time-based split: keep 2025 data as test set
test_data = data[data['year'] == 2024]

# Define features and target
features = [col for col in data.columns if col != 'value']
X_test = test_data[features]
y_test = test_data['value']

# Load the trained model from MLflow
# Get the latest run from the experiment
experiment = mlflow.get_experiment_by_name("Electricity Forecasting")
runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
latest_run = runs.iloc[0]  # Assuming the first is the latest
run_id = latest_run.run_id
model_uri = f"runs:/{run_id}/model"
model = mlflow.sklearn.load_model(model_uri)

# Make predictions
y_pred = model.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Log metrics to MLflow
with mlflow.start_run():
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("r2", r2)

print(f"MSE: {mse}")
print(f"R2: {r2}")
