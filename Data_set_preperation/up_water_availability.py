import pandas as pd

# STEP 1: Load your Excel dataset
df = pd.read_excel("/Users/g.vidyasagarreddy/Desktop/SCA_development/soil_nutrients_updated.xlsx")

# STEP 2: Water availability mapping
water_map = {
    "chickpea": "Low",
    "pigeonpeas": "Low",
    "mothbeans": "Low",
    "mungbean": "Low",
    "blackgram": "Low",
    "lentil": "Low",

    "maize": "Medium",
    "kidneybeans": "Medium",
    "cotton": "Medium",
    "coffee": "Medium",
    "coconut": "Medium",

    "rice": "High",
    "banana": "High",
    "pomegranate": "High",
    "mango": "High",
    "grapes": "High",
    "watermelon": "High",
    "muskmelon": "High",
    "apple": "High",
    "orange": "High",
    "papaya": "High",
    "jute": "High"
}

# STEP 3: Fill water_availability column automatically
df["water_availability"] = df["label"].map(water_map)

# STEP 4: Save updated Excel
df.to_excel("soil_nutrients_updated1.xlsx", index=False)

print("✅ Water availability column filled successfully!")
