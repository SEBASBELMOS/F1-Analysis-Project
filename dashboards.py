import streamlit as st
import pandas as pd

# Title
st.title("Formula 1 Lap Time Analysis Dashboard")

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("data/monza_2023_laps.csv")

    # Function to convert time strings to seconds
    def time_to_seconds(column):
        return pd.to_timedelta(column, errors='coerce').dt.total_seconds()

    # Clean time-related columns
    time_columns = ['LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time']
    for col in time_columns:
        if col in df.columns:
            df[col] = time_to_seconds(df[col])

    # Ensure LapNumber and Position are numeric
    df['LapNumber'] = pd.to_numeric(df['LapNumber'], errors='coerce')
    df['Position'] = pd.to_numeric(df['Position'], errors='coerce')

    # Drop rows with missing LapTime, LapNumber, or Driver
    df = df.dropna(subset=['LapTime', 'LapNumber', 'Driver'])

    return df

# Load cleaned data
df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
drivers = df['Driver'].unique()
selected_driver = st.sidebar.selectbox("Select a Driver:", drivers)

# Filtered data
filtered_df = df[df['Driver'] == selected_driver]

# Display filtered data
st.write(f"### Data for Driver: {selected_driver}")
st.dataframe(filtered_df)

# Line chart for Lap Times
st.write("### Lap Time Trend")
st.line_chart(filtered_df[['LapNumber', 'LapTime']].set_index('LapNumber'))

# Summary statistics
st.write("### Summary Statistics")
st.write(filtered_df.describe())
