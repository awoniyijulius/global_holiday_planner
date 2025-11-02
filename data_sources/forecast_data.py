import requests
import pandas as pd

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_forecast(lat: float, lon: float, days: int = 14) -> pd.DataFrame:
    """
    Fetch daily weather forecast for the next `days` days.
    Returns a DataFrame with columns: tavg, prcp, tsun, wspd
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,sunshine_duration",
        "timezone": "auto"
    }

    # Open-Meteo forecast API only supports up to 16 days ahead
    if days > 16:
        days = 16

    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    data = resp.json()

    if "daily" not in data:
        return pd.DataFrame()

    daily = data["daily"]
    df = pd.DataFrame({
        "time": pd.to_datetime(daily["time"]),
        "tavg": (pd.Series(daily["temperature_2m_max"]) + pd.Series(daily["temperature_2m_min"])) / 2,
        "prcp": daily.get("precipitation_sum", [None] * len(daily["time"])),
        "wspd": daily.get("windspeed_10m_max", [None] * len(daily["time"])),
        "tsun": daily.get("sunshine_duration", [None] * len(daily["time"]))
    })
    df = df.set_index("time")
    return df
