import pandas as pd
import numpy as np

def load_energy_data(file_path):
    """
    Load energy consumption data from a JSON file.

    Parameters:
    file_path (str): The path to the JSON file containing energy data.

    Returns:
    pd.DataFrame: A DataFrame containing the energy data.
    """
    return pd.read_json(file_path)


def process_energy_data(df):
    """
    Process the energy consumption data.

    Parameters:
    df (pd.DataFrame): The raw energy data DataFrame.

    Returns:
    pd.DataFrame: The processed energy data DataFrame.
    """
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Set timestamp as index
    df.set_index('timestamp', inplace=True)

    
    return df


def create_features(df):
    """
    Create additional features for the energy consumption data.

    Parameters:
    df (pd.DataFrame): The processed energy data DataFrame.

    Returns:
    pd.DataFrame: The DataFrame with additional features.
    """
    ## Create time-based features
    df['hour'] = df.index.hour
    df['day_of_week'] = df.index.dayofweek
    df['day_of_month'] = df.index.day
    df['month'] = df.index.month
    df['is_weekend'] = df.index.dayofweek >= 5
    df['year'] = df.index.year

    # cyclical encoding
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['day_of_week_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['day_of_week_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)  
    df['day_of_month_sin'] = np.sin(2 * np.pi * df['day_of_month'] / 31)
    df['day_of_month_cos'] = np.cos(2 * np.pi * df['day_of_month'] / 31)


    # Lag features
    for lag in range(1, 25):
        df[f'lag_{lag}'] = df['value'].shift(lag)

    # drop time-based features after encoding
    df.drop(columns=['hour', 'day_of_week', 'month', 'day_of_month'], inplace=True)

    # Drop rows with NaN values created by lag features
    df.dropna(inplace=True)
    
    return df

# full pipeline function
def prepare_energy_data(file_path):
    """
    Full pipeline to load, process, and create features for energy data.

    Parameters:
    file_path (str): The path to the JSON file containing energy data.

    Returns:
    pd.DataFrame: The final DataFrame ready for modeling.
    """
    df = load_energy_data(file_path)
    df = process_energy_data(df)
    df = create_features(df)
    return df

# usage with try-except block
if __name__ == "__main__":
    try:
        data_file = 'data/raw/energy_data.json'
        energy_data = prepare_energy_data(data_file)
        print("Data preparation successful. Sample data:")
        energy_data.to_csv('data/processed/energy_data_processed.csv', index=True, header=True)
        print(energy_data.head())
    except Exception as e:
        print(f"An error occurred during data preparation: {e}")
