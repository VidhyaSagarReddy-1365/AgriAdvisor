import pickle
import traceback

with open("backend/models/prophet_models/Papaya_prophet.pkl", "rb") as f:
    try:
        model = pickle.load(f)
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        print("Success! Price:", forecast["yhat"].iloc[-1])
    except Exception as e:
        print("Error during predict:")
        traceback.print_exc()
