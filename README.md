# public_building_helsinki_electricity_forecasting
This repo contains electricity data from Päiväkoti Les Galopins, Helsinki using Nuuka open API. Analysis and ML forecasting of electricity data is the focus of this repo.

### Data Ingestion
 I am using the following url to fetch the electricity data. This is and open API by city of Helsinki. Data range is from January 01, 2020 - November 30, 2025 with 1 hour interval.

 
  "https://helsinki-openapi.nuuka.cloud/api/v1.0/EnergyData/Hourly/ListByProperty?Record=LocationName&SearchString=3507&ReportingGroup=Electricity&StartTime=2020-01-01&EndTime=2025-11-30"

Data is in json format and has following metadata: 

    {
        "timestamp": "2020-01-01T00:00:00",
        "reportingGroup": "Electricity",
        "locationName": "3507 Hanuripolku 3, P\u00e4iv\u00e4koti Les Galopins",
        "value": 2.19,
        "unit": "kWh"
    }

### Data processing

Data has been processed with the data_processing.py pipeline. Raw json file was loaded and timestamp column was set as index and then time-based features are constructed. With time-based features; cyclic features are constructed and redundant features were dropped. 

Then lagged features (3 lags) are created. Lag features play a crucial role in forecasting where there is a schedule. This is a school building, so it follows a schedule.

Processed data has been stored as csv file in data/processed directory and we are going to use this data for modeling and forecasting.

### Model Training

The model training is handled by src/training.py. It uses RandomForestRegressor with GridSearchCV for hyperparameter tuning. The data is split time-based, with 2024 data as the test set. MLflow is used for experiment tracking, logging parameters, and the trained model.

User needs to run python src/training.py to initiate MLflow and train the model and save it using MLflow. It will create a folder named "mlruns".

User can see MLflow using command "mlflow ui".

### Model Evaluation

Model evaluation is performed by src/evaluation.py. It loads the trained model from MLflow, makes predictions on the test set, calculates MSE and R2 metrics, and logs them back to MLflow.

### API

A FastAPI application is available in api/main.py to serve predictions. It exposes a /predict endpoint that accepts feature inputs and returns electricity consumption predictions using the trained model loaded from MLflow.

To run the API:
```
uvicorn api.main:app --reload
```
The API will be available at http://127.0.0.1:8000.


### UI

A Streamlit UI is provided in ui/app.py for interactive predictions and evaluation display. It allows users to input features, call the FastAPI for predictions, and view model evaluation results.

To run the UI:
```
streamlit run ui/app.py
```

### Requirements

Install dependencies:
```
pip install -r requirements.txt
```

