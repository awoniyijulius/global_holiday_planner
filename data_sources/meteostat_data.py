import pandas as pd
from meteostat import Daily, Stations
from datetime import datetime

# Coordinates for supported cities
CITIES_COORDS = {
    "London (Heathrow)": (51.4700, -0.4543),
    "Paris (CDG)": (49.0097, 2.5479),
    "New York (JFK)": (40.6413, -73.7781),
    "Sydney (Kingsford Smith)": (-33.9399, 151.1753),
    "Lagos (Murtala Muhammed)": (6.5770, 3.3212),
    "Tokyo (Haneda)": (35.5494, 139.7798),
    "São Paulo (GRU)": (-23.4356, -46.4731),
    "Cape Town (CPT)": (-33.9696, 18.5972),
    "Toronto (YYZ)": (43.6777, -79.6248),
    "Dubai (DXB)": (25.2532, 55.3657),
}

def get_nearest_station(lat: float, lon: float):
    """Find the nearest weather station to given coordinates."""
    stations = Stations().nearby(lat, lon).fetch()
    if stations.empty:
        return None
    return stations.index[0], stations.iloc[0]

def fetch_daily(station_id: str, year: int) -> pd.DataFrame:
    """Fetch daily weather data for a given station and year."""
    start, end = datetime(year, 1, 1), datetime(year, 12, 31)
    df = Daily(station_id, start, end).fetch()
    df.index.name = "time"
    return df

def historical_for_city(city: str, year: int) -> pd.DataFrame:
    """Get daily weather data for a city and year."""
    lat, lon = CITIES_COORDS[city]
    station = get_nearest_station(lat, lon)
    if station is None:
        return pd.DataFrame()
    station_id, _meta = station
    df = fetch_daily(station_id, year)
    return df
