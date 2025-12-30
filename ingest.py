import requests
import json

def fetch_data(url):
    '''
    Fetches JSON data from the given URL.

    :param url: The URL to fetch data from.
    :return: A dictionary containing the JSON response, or None if an error occurs.
    '''
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    url = "https://helsinki-openapi.nuuka.cloud/api/v1.0/EnergyData/Hourly/ListByProperty?Record=LocationName&SearchString=3507&ReportingGroup=Electricity&StartTime=2020-01-01&EndTime=2025-11-30"
    data = fetch_data(url)
    if data:
        data_json = json.dumps(data, indent=4)
        with open("data/raw/energy_data.json", "w") as file:
            file.write(data_json)
