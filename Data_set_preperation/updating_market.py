import pandas as pd

# STEP 1: Load your Excel dataset
df = pd.read_excel("soil_nutrients_updated1.xlsx")

# =====================================================
# STEP 2: Market Type Mapping (YOUR DATA ONLY)
# =====================================================

market_type_map = {

    # 🌾 Cereals & Pulses → Wholesale/Mandi
    "rice": "Government Mandi/Wholesale",
    "maize": "Wholesale/Feed Industry",
    "chickpea": "Mandi/Wholesale",
    "kidneybeans": "Wholesale Market",
    "pigeonpeas": "Mandi",
    "mothbeans": "Mandi",
    "mungbean": "Wholesale",
    "blackgram": "Wholesale",
    "lentil": "Wholesale",

    # 🍎 Fruits → Retail/Export
    "banana": "Retail/City Market/Processing",
    "mango": "Retail/Export",
    "grapes": "Export/Wine Industry",
    "watermelon": "Local Retail Market",
    "muskmelon": "Local Retail Market",
    "papaya": "Retail Market",
    "orange": "Retail/Processing",
    "apple": "Wholesale/Retail",
    "pomegranate": "Export/Retail",
    "coconut": "Wholesale/Processing",

    # 🌱 Cash Crops → Industry
    "cotton": "Textile Mills/Industry",
    "jute": "Jute Processing Industry",
    "coffee": "Processing/Export"
}

# =====================================================
# STEP 3: Market Distance Mapping (YOUR DATA ONLY)
# =====================================================

market_distance_map = {

    # Cereals & Pulses
    "rice": "50-300 km",
    "maize": "50-200 km",
    "chickpea": "50-300 km",
    "kidneybeans": "50-200 km",
    "pigeonpeas": "50-300 km",
    "mothbeans": "100-300 km",
    "mungbean": "50-200 km",
    "blackgram": "50-200 km",
    "lentil": "50-300 km",

    # Fruits
    "banana": "0-50 km",
    "mango": "0-100 km",
    "grapes": "0-100 km",
    "watermelon": "0-30 km",
    "muskmelon": "0-30 km",
    "papaya": "0-50 km",
    "orange": "0-100 km",
    "apple": "50-200 km",
    "pomegranate": "50-150 km",
    "coconut": "50-200 km",

    # Cash Crops
    "cotton": "50-300 km",
    "jute": "50-200 km",
    "coffee": "0-150 km"
}

# =====================================================
# STEP 4: Fill columns automatically
# =====================================================

df["Market_Type"] = df["label"].map(market_type_map)
df["Market_distance "] = df["label"].map(market_distance_map)

# =====================================================
# STEP 5: Save updated Excel
# =====================================================

df.to_excel("soil_nutrients_updated2.xlsx", index=False)

print("✅ Market type and market distance added successfully!")
