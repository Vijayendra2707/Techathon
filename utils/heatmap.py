import numpy as np
from sklearn.neighbors import KernelDensity

def build_severity_heatmap(df):

    severity_weights = {
        1: 1,
        2: 3,
        3: 6
    }

    df = df.copy()
    df["weight"] = df["Accident_Severity"].map(severity_weights).fillna(1)

    coords = df[["latitude","longitude"]].values
    weights = df["weight"].values

    kde = KernelDensity(
        bandwidth=0.01,
        kernel="gaussian"
    )

    kde.fit(coords, sample_weight=weights)

    density = np.exp(kde.score_samples(coords))

    df["density"] = density

    df["heat_intensity"] = (
        df["density"] - df["density"].min()
    ) / (
        df["density"].max() - df["density"].min()
    )

    heatmap_data = df[
        ["latitude","longitude","heat_intensity"]
    ].values.tolist()

    return heatmap_data