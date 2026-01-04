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

Then lagged features (24 lags) are created. Lag features play a crucial role in forecasting where there is a schedule. This is a school building, so it follows a schedule.

Processed data has been stored as csv file in data/processed directory and we are going to use this data for modeling and forecasting.

### Model Training 

