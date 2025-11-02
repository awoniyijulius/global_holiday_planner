import streamlit as st
from data_sources.meteostat_data import CITIES_COORDS

def controls():
    # Use the dictionary keys directly so they match perfectly
    city = st.selectbox("Select a city", list(CITIES_COORDS.keys()))
    year = st.number_input("Year", min_value=2000, max_value=2100, value=2024, step=1)
    top_n = st.slider("Top weeks to display", 1, 5, 2)
    hemisphere = st.radio("Hemisphere", ["Northern (Jun–Aug)", "Southern (Dec–Feb)"], index=0)
    summer_only = st.checkbox("Restrict to summer months", value=True)
    return city, year, top_n, hemisphere, summer_only
