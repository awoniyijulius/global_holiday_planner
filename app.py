import streamlit as st

# --- Page setup (must be first Streamlit command) ---
st.set_page_config(page_title="Global Holiday Planner", page_icon="🌍", layout="wide")

import pandas as pd
from ui.components import controls
from data_sources.meteostat_data import historical_for_city, CITIES_COORDS
from data_sources.forecast_data import fetch_forecast
from logic.scoring import add_scores
from logic.blending import weekly_scores
from ui.charts import weekly_trend_chart, heatmap_chart

# --- Background and styling ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.85);
}
h1 {
    color: #ffffff !important;
    text-shadow: 0 2px 6px rgba(0,0,0,0.6);
}

/* Fade-in animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px);}
    to   { opacity: 1; transform: translateY(0);}
}
.panel {
    background: rgba(0,0,50,0.35);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 25px;
    animation: fadeIn 1s ease-out;
}
.results-table { width: 100%; border-collapse: collapse; backdrop-filter: blur(3px);}
.results-table th, .results-table td {
    padding: 10px 12px;
    border-bottom: 1px solid rgba(255,255,255,0.15);
    color: #fff;
}
.results-table th {
    text-align: left;
    background: rgba(0,0,0,0.35);
    font-weight: 600;
}
.row-forecast { background: rgba(0, 128, 0, 0.25);}
.row-historical { background: rgba(0, 0, 128, 0.25);}
.results-table tr:hover { background: rgba(255,255,255,0.10);}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Title ---
st.markdown('<h1>🌍 Global Holiday Planner</h1>', unsafe_allow_html=True)
st.write("Find the best holiday weeks based on temperature, rainfall, sunshine, and wind.")
st.divider()

# --- UI controls ---
city, year, top_n, hemisphere, summer_only = controls()
use_forecast = st.checkbox("Include forecast data", value=True)
st.divider()

# --- Data pipeline ---
df = historical_for_city(city, year)

if df.empty:
    st.error("No data available for this city/year.")
else:
    # Summer filter
    if summer_only:
        if "Northern" in hemisphere:
            df = df.loc[f"{year}-06-01":f"{year}-08-31"]
        else:
            df = df.loc[f"{year-1}-12-01":f"{year}-02-28"]

    # Add scores
    df = add_scores(df)

    # Forecast
    if use_forecast:
        lat, lon = CITIES_COORDS[city]
        forecast_df = fetch_forecast(lat, lon, days=16)
        if not forecast_df.empty:
            forecast_df = add_scores(forecast_df)
            df = pd.concat([df, forecast_df])

    # Weekly aggregation
    weekly = weekly_scores(df, top_n=top_n)

    # --- Results panel ---
    st.markdown(f"<div class='panel'><h3 style='color:white;'>Top {top_n} holiday weeks — {city} ({year})</h3>", unsafe_allow_html=True)

    if weekly.empty:
        st.info("No weekly scores available.")
    else:
        weekly_display = weekly.reset_index()
        weekly_display["week_start"] = pd.to_datetime(weekly_display["week_start"]).dt.strftime("%Y-%m-%d")

        # CSV export
        csv = weekly_display.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download as CSV", data=csv, file_name=f"{city}_{year}_holiday_weeks.csv", mime="text/csv")

        # Styled HTML table
        rows = []
        for _, r in weekly_display.iterrows():
            cls = "row-forecast" if str(r.get("source")) == "Forecast" else "row-historical"
            rows.append(
                f"<tr class='{cls}'><td>{r['week_start']}</td>"
                f"<td>{round(float(r['holiday_score']),2)}</td>"
                f"<td>{r['source']}</td></tr>"
            )
        table_html = f"""
        <table class="results-table">
            <thead><tr><th>Start</th><th>Score</th><th>Source</th></tr></thead>
            <tbody>{''.join(rows)}</tbody>
        </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # --- Daily preview ---
    st.markdown("<div class='panel'><h3 style='color:white;'>Preview of daily data with scores</h3>", unsafe_allow_html=True)
    st.dataframe(df.head(20))
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Charts ---
    st.subheader("Charts")
    weekly_trend_chart(weekly)
    heatmap_chart(df)
