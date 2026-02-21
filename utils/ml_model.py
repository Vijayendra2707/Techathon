from sklearn.ensemble import RandomForestClassifier


FEATURES = [
    "Speed_limit",
    "Number_of_Vehicles",
    "hour",
    "bad_weather",
    "dark"
]


def train_model(df):

    X = df[FEATURES]
    y = df["accident_label"]

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=14,
        class_weight="balanced",   # ⭐ MAGIC LINE
        n_jobs=-1,
        random_state=42
    )

    model.fit(X, y)

    return model