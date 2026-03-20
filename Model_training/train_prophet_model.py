import pandas as pd
from prophet import Prophet
import pickle
import os

print("Loading price dataset...")

df = pd.read_csv("crop_prices_india.csv")

df["Date"] = pd.to_datetime(df["Date"])

os.makedirs("prophet_models", exist_ok=True)

crops = df["Crop"].unique()

for crop in crops:

    print(f"Training Prophet model for {crop}")

    crop_df = df[df["Crop"] == crop]

    prophet_df = crop_df[["Date","Price"]].copy()
    prophet_df.columns = ["ds","y"]

    prophet_df = prophet_df.sort_values("ds")

    model = Prophet()

    model.fit(prophet_df)

    with open(f"prophet_models/{crop}_prophet.pkl","wb") as f:
        pickle.dump(model,f)

    print(f"{crop} model saved")

print("All Prophet models trained successfully")