import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium import Icon
# Title of the app
st.title("Home Health Agencies in RI-MA Region")

# Pre-defined data (replace with the actual file path)
file_path = "RI-MA-HHAS-With-Coordinates.csv"

# Load the data into a DataFrame
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"File not found at path: {file_path}")
    st.stop()

# Display the table
st.subheader("Data Table")
st.dataframe(df)

# Check if Latitude and Longitude columns exist
if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
    st.error("The dataset must contain 'Latitude' and 'Longitude' columns for mapping.")
    st.stop()

# Create a Folium map centered around the average latitude and longitude
try:
    avg_latitude = df['Latitude'].mean()
    avg_longitude = df['Longitude'].mean()
except Exception as e:
    st.error(f"Error calculating average latitude and longitude: {e}")
    st.stop()

m = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=10)

# Add markers for each location in the dataset
for idx, row in df.iterrows():
    if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"<b>{row['Name']}</b><br>{row['Primary Practice Address']}<br>{row['Phone']}",
            tooltip=row['Name'],
            icon=Icon(icon='home', prefix='fa')
        ).add_to(m)

# Display the Folium map in Streamlit
st.subheader("Map of Locations")
st_folium(m, width=700, height=500)
