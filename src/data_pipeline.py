import fastf1
import pandas as pd
import os

def fetch_and_process_race_data(cache_dir='data/cache', output_dir='data/processed'):
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(cache_dir)

    races = [
        {'year': 2025, 'location': 'Bahrain'},
        {'year': 2025, 'location': 'Monaco'},
        {'year': 2025, 'location': 'Silverstone'},
        {'year': 2025, 'location': 'Monza'},
        {'year': 2025, 'location': 'Suzuka'}
    ]

    all_merged_laps = []

    for race in races:
        print(f"Fetching {race['year']} {race['location']}...")
        session = fastf1.get_session(race['year'], race['location'], 'R')
        session.load(telemetry=True, weather=True)
        
        laps = session.laps.copy()
        weather = session.weather_data.copy()
        laps['Race'] = race['location']
        laps['Year'] = race['year']
        
        laps = laps.dropna(subset=['LapTime', 'Driver']).copy()
        laps['LapTime_s'] = laps['LapTime'].dt.total_seconds()
        
        laps['Time_sec'] = pd.to_timedelta(laps['Time']).dt.total_seconds()
        weather['Time_sec'] = pd.to_timedelta(weather['Time']).dt.total_seconds()
        
        laps = laps.sort_values('Time_sec')
        weather = weather.sort_values('Time_sec')
        
        merged_race = pd.merge_asof(
            laps, 
            weather, 
            on='Time_sec', 
            direction='nearest'
        )
        
        all_merged_laps.append(merged_race)

    final_dataset = pd.concat(all_merged_laps, ignore_index=True)
    
    os.makedirs(output_dir, exist_ok=True)
    final_dataset.to_csv(f'{output_dir}/cleaned_laps.csv', index=False)
    print("Pipeline complete. Unified CSV saved to data/processed/cleaned_laps.csv")

if __name__ == "__main__":
    fetch_and_process_race_data()