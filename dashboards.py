import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned data
@st.cache_data
def load_data():
    return pd.read_csv("data/monza_2023_laps_cleaned.csv")

df = load_data()

# Title
st.title("Formula 1 Lap Time Analysis Dashboard")

# Sidebar: Select Driver
st.sidebar.header("Filter Data")
drivers = df['Driver'].unique()
selected_driver = st.sidebar.selectbox("Select a Driver:", drivers)

# Fastest Lap - Sorted
st.write("### Fastest Lap for Each Driver")
fastest_laps = df.groupby('Driver')['LapTime'].min().reset_index()
fastest_laps = fastest_laps.sort_values(by='LapTime')  # Sort by LapTime (ascending)
st.dataframe(fastest_laps.reset_index(drop=True))

# Highlight Fastest Lap for Selected Driver
st.write(f"### Fastest Lap for {selected_driver}")
fastest_lap = df[df['Driver'] == selected_driver]['LapTime'].min()
st.write(f"**{selected_driver}**'s fastest lap time: {fastest_lap:.2f} seconds")

# Lap Time Trend
st.write(f"### Lap Time Trend for {selected_driver}")
driver_data = df[df['Driver'] == selected_driver]

fig, ax = plt.subplots()
ax.plot(driver_data['LapNumber'], driver_data['LapTime'], marker='o', linestyle='-')
ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time (seconds)")
ax.set_title(f"Lap Time Trend for {selected_driver}")
st.pyplot(fig)

# Average Sector Times - Sorted
st.write("### Average Sector Times for Drivers")
sector_times = df.groupby('Driver')[['Sector1Time', 'Sector2Time', 'Sector3Time']].mean().reset_index()
sector_times['AverageSectorTime'] = sector_times[['Sector1Time', 'Sector2Time', 'Sector3Time']].mean(axis=1)
sector_times = sector_times.sort_values(by='AverageSectorTime')  # Sort by average sector time

# Function to style minimum values
def highlight_min(s):
    is_min = s == s.min()
    return ['background-color: lightgreen; color: black' if v else '' for v in is_min]

# Apply styling
styled_sector_times = sector_times.style.apply(highlight_min, subset=['Sector1Time', 'Sector2Time', 'Sector3Time'])

# Display table
#st.write("### Highlighted Average Sector Times")
st.dataframe(styled_sector_times)