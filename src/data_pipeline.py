import fastf1
import pandas as pd
import os

def fetch_and_process_race_data(cache_dir='data/cache', output_dir='data/processed'):
    # Enable caching to store API requests locally
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(cache_dir)

    # Define the 5 races for the dataset
    races = [
        {'year': 2023, 'location': 'Bahrain'},
        {'year': 2023, 'location': 'Monaco'},
        {'year': 2023, 'location': 'Silverstone'},
        {'year': 2023, 'location': 'Monza'},
        {'year': 2023, 'location': 'Suzuka'}
    ]

    all_laps = []
    all_weather = []

    for race in races:
        print(f"Fetching {race['year']} {race['location']}...")
        session = fastf1.get_session(race['year'], race['location'], 'R')
        session.load(telemetry=True, weather=True)
        
        # Extract Laps
        laps = session.laps
        laps['Race'] = race['location']
        laps['Year'] = race['year']
        
        # Extract Weather
        weather = session.weather_data
        weather['Race'] = race['location']
        weather['Year'] = race['year']
        
        all_laps.append(laps)
        all_weather.append(weather)

    # Combine all race data
    combined_laps = pd.concat(all_laps, ignore_index=True)
    combined_weather = pd.concat(all_weather, ignore_index=True)

    # Clean the telemetry (drop missing driver/lap data and calculate raw seconds)
    cleaned_laps = combined_laps.dropna(subset=['LapTime', 'Driver'])
    cleaned_laps['LapTime_s'] = cleaned_laps['LapTime'].dt.total_seconds()

    # Export to the processed folder for Members 2 & 4
    os.makedirs(output_dir, exist_ok=True)
    cleaned_laps.to_csv(f'{output_dir}/cleaned_laps.csv', index=False)
    combined_weather.to_csv(f'{output_dir}/weather_data.csv', index=False)
    print("Pipeline execution complete. CSVs saved to data/processed/")

if __name__ == "__main__":
    fetch_and_process_race_data()
    