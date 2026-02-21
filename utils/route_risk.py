import numpy as np
from utils.ml_model import FEATURES


def compute_route_risk(route_points, model):

    risks = []

    sampled = route_points[::20]

    for lat, lon in sampled:

        # dummy environmental assumptions
        features = {
            "Speed_limit": 50,
            "Number_of_Vehicles": 2,
            "hour": 18,
            "bad_weather": 0,
            "dark": 0
        }

        X = [[features[f] for f in FEATURES]]

        prob = model.predict_proba(X)[0][1]

        risks.append(prob)

    return float(np.mean(risks))