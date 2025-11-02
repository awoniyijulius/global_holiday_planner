import pandas as pd

def score_day_safe(row: pd.Series) -> int:
    score = 0
    tavg, prcp, tsun, wspd = row.get("tavg"), row.get("prcp"), row.get("tsun"), row.get("wspd")

    if pd.notna(tavg):
        if 20 <= tavg <= 27:
            score += 2
        elif (15 <= tavg < 20) or (28 <= tavg <= 30):
            score += 1

    if pd.notna(prcp):
        if prcp <= 1:
            score += 2
        elif prcp <= 5:
            score += 1

    if pd.notna(tsun):
        if tsun > 300:
            score += 2
        elif tsun >= 150:
            score += 1

    if pd.notna(wspd):
        if wspd < 20:
            score += 1

    return score

def add_scores(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    df["holiday_score"] = df.apply(score_day_safe, axis=1)
    return df
