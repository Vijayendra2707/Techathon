import pandas as pd

def create_dashboard_metrics(df):

    # Dynamic thresholds
    high_threshold = df["risk_score"].quantile(0.85)
    medium_threshold = df["risk_score"].quantile(0.60)

    metrics = {
        "avg_risk_score": round(df["risk_score"].mean(), 2),
        "avg_prediction": round(df["risk_probability"].mean(), 3),
        "high_risk_count": int((df["risk_score"] >= high_threshold).sum()),
        "total_accidents": len(df)
    }

    # Risk distribution
    risk_bins = {
        "Safe": int((df["risk_score"] < medium_threshold).sum()),
        "Medium": int(((df["risk_score"] >= medium_threshold) &
                       (df["risk_score"] < high_threshold)).sum()),
        "High Risk": int((df["risk_score"] >= high_threshold).sum())
    }

    # Day counts
    day_counts = df["Day_of_Week"].value_counts().to_dict()

    # Road risk
    road_risk = (
        df.groupby("Road_Type")["risk_score"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .to_dict()
    )

    return metrics, day_counts, risk_bins, road_risk