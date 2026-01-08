import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
import mlflow
import mlflow.sklearn
from data_processing import load_processed_energy_data

# Load processed data
data = load_processed_energy_data()

# Time-based split: keep 2024 data as test set
train_data = data[data['year'] < 2024]
test_data = data[data['year'] == 2024]

# Define features and target
features = [col for col in data.columns if col != 'value']
X_train = train_data[features]
y_train = train_data['value']
X_test = test_data[features]
y_test = test_data['value']

# Initiate MLflow tracking
mlflow.set_experiment("Electricity Forecasting")
with mlflow.start_run():
    # Define the model
    rf = RandomForestRegressor(random_state=42)

    # Define parameter grid for GridSearchCV
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    # Perform GridSearchCV with cv=5
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # Get the best model
    best_model = grid_search.best_estimator_

    # Log all GridSearchCV parameters, best parameters, and model
    mlflow.log_params({"param_grid": param_grid})
    mlflow.log_params(grid_search.best_params_)
    mlflow.sklearn.log_model(best_model, "model")

    print(f"Best parameters: {grid_search.best_params_}")
