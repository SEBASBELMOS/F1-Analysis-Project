import os
import fastf1 as f1

# Check if the 'cache' folder exists; if not, create it
cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# Enable FastF1 cache
f1.Cache.enable_cache(cache_dir)

# Fetch session data
race = f1.get_session(2023, 'Monza', 'R')  # Example: Monza 2023 GP
race.load()

print(race.results)  # Print Driver standings to console

# Ensure 'data' folder exists before saving the CSV
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Directly save laps data to CSV
laps_df = race.laps  # Laps object is already a DataFrame-like structure
csv_path = os.path.join(data_dir, 'monza_2023_laps.csv')  # Full path to save CSV
laps_df.to_csv(csv_path, index=False)  # Save DataFrame to CSV without index

print(f"Laps data saved successfully to {csv_path}")
