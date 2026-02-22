import pandas as pd
import joblib

from data_processing import load_data
from feature_engineering import create_features,generate_negative_samples
from ml_model import train_model

print("Loading data...")
df = load_data("data/pune_cleaned_dataset.csv")

print("Creating features...")
df = create_features(df)

print("Generating negative samples...")
negative_df = generate_negative_samples(df)

full_df = pd.concat([df, negative_df])

print("Training model...")
model = train_model(full_df)

# SAVE MODEL
joblib.dump(model, "model.pkl")

print("✅ Model saved successfully")