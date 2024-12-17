import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Title
st.title("🏎️ Formula 1 Lap Time Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/monza_2023_laps.csv")

    # Clean time-related columns
    time_columns = ['Sector3Time', 'Sector1SessionTime', 'Sector2SessionTime', 'Sector3SessionTime']

    for col in time_columns:
        if col in df.columns:
            df[col] = pd.to_timedelta(df[col], errors='coerce').dt.total_seconds()

    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
drivers = df['Driver'].unique()
selected_driver = st.sidebar.selectbox("Select a Driver:", drivers)

# Filtered data
filtered_df = df[df['Driver'] == selected_driver]
st.write(f"### Data for Driver: {selected_driver}")
st.dataframe(filtered_df)

# Line chart for lap times
st.write("### Lap Time Trend")
fig, ax = plt.subplots()
ax.plot(filtered_df['LapNumber'], filtered_df['LapTime'], marker='o', linestyle='-', label=selected_driver)
ax.set_xlabel("Lap Number")
ax.set_ylabel("Lap Time (s)")
ax.set_title(f"Lap Times for {selected_driver}")
ax.legend()
st.pyplot(fig)

# Summary statistics
st.write("### Summary Statistics")
st.write(filtered_df.describe())

# Interactive scatter plot
st.write("### Sector Times vs Lap Number")
fig = px.scatter(
    filtered_df, 
    x='LapNumber', 
    y='Sector3Time', 
    title=f"Sector 3 Times for {selected_driver} (in Seconds)",
    labels={'Sector3Time': 'Sector 3 Time (s)'}
)
st.plotly_chart(fig)
