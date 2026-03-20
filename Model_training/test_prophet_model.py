import pickle
import pandas as pd

def predict_future_price(crop_name):

    try:
        with open(f"prophet_models/{crop_name}_prophet.pkl","rb") as f:
            model = pickle.load(f)

        future = model.make_future_dataframe(periods=30)

        forecast = model.predict(future)

        future_price = forecast["yhat"].iloc[-1]

        return round(future_price,2)

    except:
        return "Price model not available"