import pandas as pd

# STEP 1: Load your Excel file
df = pd.read_excel("/Users/g.vidyasagarreddy/Desktop/SCA_development/soil nutients data.xlsx")

# STEP 2: Create irrigation mapping
irrigation_map = {
    "rice": "Flood",
    "maize": "Furrow",
    "chickpea": "Rainfed",
    "kidneybeans": "Furrow",
    "pigeonpeas": "Rainfed",
    "mothbeans": "Rainfed",
    "mungbean": "Furrow",
    "blackgram": "Rainfed",
    "lentil": "Rainfed",
    "pomegranate": "Drip",
    "banana": "Drip",
    "mango": "Drip",
    "grapes": "Drip",
    "watermelon": "Drip",
    "muskmelon": "Drip",
    "apple": "Sprinkler",
    "orange": "Drip",
    "papaya": "Drip",
    "coconut": "Basin",
    "coffee": "Sprinkler",
    "cotton": "Furrow",
    "jute": "Flood"
}

# STEP 3: Add new column automatically
df["irrigation_type"] = df["label"].map(irrigation_map)

# STEP 4: Save updated Excel file
df.to_excel("soil_nutrients_updated.xlsx", index=False)

print("✅ Irrigation column added successfully!")
