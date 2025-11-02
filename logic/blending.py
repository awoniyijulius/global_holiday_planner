import pandas as pd

def weekly_scores(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Aggregate daily scores into weekly averages.
    Labels each week as 'Historical' or 'Forecast' depending on the date.
    """
    if df.empty or "holiday_score" not in df.columns:
        return pd.DataFrame()

    # Copy to avoid modifying original
    df = df.copy()

    # Mark rows as forecast if their index is in the future
    today = pd.Timestamp.today().normalize()
    df["source"] = df.index.map(lambda d: "Forecast" if d >= today else "Historical")

    # Weekly aggregation
    weekly = (
        df.groupby([pd.Grouper(freq="W-MON"), "source"])["holiday_score"]
        .mean()
        .reset_index()
        .rename(columns={"time": "week_start"})
    )

    # Sort by score and pick top_n
    weekly = weekly.sort_values("holiday_score", ascending=False).head(top_n)
    weekly = weekly.set_index("week_start")

    return weekly
