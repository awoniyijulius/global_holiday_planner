import streamlit as st
import altair as alt
import pandas as pd

# A helper to wrap charts in a styled container
def chart_container(title: str, chart):
    st.markdown(
        f"""
        <div style="
            background: rgba(0,0,50,0.35);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 25px;
        ">
            <h3 style="color:white; margin-top:0;">{title}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.altair_chart(chart, use_container_width=True)


def weekly_trend_chart(weekly: pd.DataFrame):
    """Plot a line chart of weekly holiday scores with polished styling."""
    if weekly.empty:
        st.warning("No weekly data to plot.")
        return

    weekly = weekly.reset_index()
    if "week_start" not in weekly.columns:
        weekly = weekly.rename(columns={weekly.columns[0]: "week_start"})
    weekly["week_start"] = pd.to_datetime(weekly["week_start"])

    chart = (
        alt.Chart(weekly)
        .mark_line(point=alt.OverlayMarkDef(color="white", size=80), strokeWidth=3)
        .encode(
            x=alt.X("week_start:T", title="Week"),
            y=alt.Y("holiday_score:Q", title="Average Holiday Score"),
            color=alt.Color(
                "source:N",
                title="Data Source",
                scale=alt.Scale(domain=["Historical", "Forecast"],
                                range=["#1f77b4", "#2ca02c"])  # blue & green
            ),
            tooltip=["week_start:T", "holiday_score:Q", "source:N"]
        )
        .configure_axis(labelColor="white", titleColor="white")
        .configure_title(color="white", fontSize=18, anchor="start")
        .configure_legend(labelColor="white", titleColor="white", orient="top")
        .properties(width=700, height=400)
    )

    chart_container("📈 Weekly Holiday Score Trend", chart)


def heatmap_chart(df: pd.DataFrame):
    """Plot a heatmap of daily holiday scores by month and day with polished styling."""
    if df.empty or "holiday_score" not in df.columns:
        st.warning("No data available for heatmap.")
        return

    df = df.reset_index().rename(columns={"time": "date"})
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%b")
    df["day"] = df["date"].dt.day

    if "source" not in df.columns:
        df["source"] = "Historical"

    chart = (
        alt.Chart(df)
        .mark_rect()
        .encode(
            x=alt.X("day:O", title="Day of Month"),
            y=alt.Y("month:O", title="Month"),
            color=alt.Color(
                "holiday_score:Q",
                scale=alt.Scale(scheme="viridis"),
                title="Score"
            ),
            tooltip=["date:T", "holiday_score:Q", "source:N"]
        )
        .configure_axis(labelColor="white", titleColor="white")
        .configure_title(color="white", fontSize=18, anchor="start")
        .properties(width=700, height=400)
    )

    chart_container("🌞 Holiday Score Heatmap", chart)
