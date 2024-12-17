import pandas as pd

# Load the data
df = pd.read_csv("data/monza_2023_laps.csv")

# Function to convert time columns to seconds
def time_to_seconds(column):
    return pd.to_timedelta(column, errors='coerce').dt.total_seconds()

# Convert relevant columns to seconds
time_columns = ['LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time']
for col in time_columns:
    if col in df.columns:
        df[col] = time_to_seconds(df[col])

# Ensure LapNumber is numeric
df['LapNumber'] = pd.to_numeric(df['LapNumber'], errors='coerce')

# Drop rows with missing essential data
df = df.dropna(subset=['LapTime', 'LapNumber', 'Driver'])

# Save the cleaned data
df.to_csv("data/monza_2023_laps_cleaned.csv", index=False)
print("Data cleaned and saved successfully!")
