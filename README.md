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