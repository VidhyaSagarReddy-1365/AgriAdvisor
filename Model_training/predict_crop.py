import pandas as pd
import joblib
import pickle

print("\n========== TESTING CROP ADVISORY SYSTEM ==========")

# ==========================================
# LOAD XGBOOST MODEL
# ==========================================
model = joblib.load("crop_model_pipeline.pkl")
label_encoder = joblib.load("crop_label_encoder.pkl")

print("Model loaded successfully")


# ==========================================
# PROPHET PRICE FUNCTION
# ==========================================
def predict_future_price(crop_name):

    try:
        with open(f"prophet_models/{crop_name}_prophet.pkl","rb") as f:
            prophet_model = pickle.load(f)

        future = prophet_model.make_future_dataframe(periods=30)

        forecast = prophet_model.predict(future)

        future_price = forecast["yhat"].iloc[-1]

        return round(future_price,2)

    except:
        return "Price model unavailable"


# ==========================================
# USER INPUT
# ==========================================
new_data = {
    "n": 50,
    "p": 35,
    "k": 30,
    "temperature": 32,
    "humidity": 60,
    "ph": 6.5,
    "rainfall": 90,
    "irrigation_type": "Drip",
    "water_availability": "high",
    "market_type": "Retail",
    "market_distance": "50-200 km"
}
# ==========================================
# STEP 1 — SOIL SUITABILITY CHECK
# ==========================================
if (
    new_data["n"] <= 5 and
    new_data["p"] <= 5 and
    new_data["k"] <= 5 and
    new_data["rainfall"] <= 5
):
    print("\n⚠ Soil not suitable for crop cultivation.")
    print("Recommendation: Improve soil fertility and irrigation first.")
    exit()


# ==========================================
# STEP 2 — INPUT VALIDATION
# ==========================================
if not (0 <= new_data["humidity"] <= 100):
    print("Invalid humidity value")
    exit()

if not (3 <= new_data["ph"] <= 10):
    print("Invalid soil pH")
    exit()


# ==========================================
# STEP 3 — MODEL PREDICTION
# ==========================================
input_df = pd.DataFrame([new_data])

probs = model.predict_proba(input_df)[0]
crop_names = label_encoder.classes_

results = pd.DataFrame({
    "Crop": crop_names,
    "Confidence": probs * 100
})

results = results.sort_values(by="Confidence", ascending=False)


# ==========================================
# STEP 4 — PRACTICAL FILTERING
# ==========================================
water = new_data["water_availability"]

if water == "Low":
    results = results[~results["Crop"].isin(["rice", "banana", "jute"])]

elif water == "High":
    pass

elif water == "Medium":
    results = results[~results["Crop"].isin(["rice"])]


# ==========================================
# STEP 5 — DYNAMIC CONFIDENCE LOGIC
# ==========================================
top_conf = results.iloc[0]["Confidence"]

print("\n========== CROP ADVISORY ==========")

recommended_crops = []

# CASE 1 — Strong
if top_conf >= 60:

    print("\n🌱 Strongly Recommended Crop:")

    crop = results.iloc[0]["Crop"]
    conf = results.iloc[0]["Confidence"]

    print(f"✔ {crop} ({conf:.2f}%)")

    recommended_crops.append((crop, conf))

    print("\nAlternative Options:")

    for i in range(1,3):
        if i < len(results):

            crop = results.iloc[i]["Crop"]
            conf = results.iloc[i]["Confidence"]

            print(f"➤ {crop} ({conf:.2f}%)")

            recommended_crops.append((crop, conf))


# CASE 2 — Moderate
elif 40 <= top_conf < 60:

    print("\n🌱 Recommended Crops:")

    for i in range(min(3,len(results))):

        crop = results.iloc[i]["Crop"]
        conf = results.iloc[i]["Confidence"]

        print(f"✔ {crop} ({conf:.2f}%)")

        recommended_crops.append((crop, conf))


# CASE 3 — Weak
else:

    print("\n⚠ No strong crop recommendation.")
    print("Showing best possible alternatives:")

    for i in range(min(3,len(results))):

        crop = results.iloc[i]["Crop"]
        conf = results.iloc[i]["Confidence"]

        print(f"➤ {crop} ({conf:.2f}%)")

        recommended_crops.append((crop, conf))

    print("\nAdvice: Conditions are uncertain for profitable farming.")


print("\n===================================")


# ==========================================
# STEP 6 — PROPHET PRICE FORECAST
# ==========================================
print("\n========== FUTURE PRICE FORECAST ==========\n")

for crop,conf in recommended_crops:

    price = predict_future_price(crop)

    print(f"{crop} | confidence: {conf:.2f}% | predicted price: ₹{price}")