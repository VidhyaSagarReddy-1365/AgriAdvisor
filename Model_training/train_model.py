# ==========================================
# STEP 1 — Import libraries
# ==========================================
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

print("\n========== LOADING DATASET ==========")

# ==========================================
# STEP 2 — Load dataset
# ==========================================
df = pd.read_csv(
    "soil_nutrients_updated.csv"
)

df.columns = df.columns.str.strip().str.lower()

print("Dataset Shape:", df.shape)

# ==========================================
# STEP 3 — Remove missing values
# ==========================================
df = df.dropna()

# ==========================================
# STEP 4 — Remove unrealistic training values
# ==========================================
df = df[
    (df["n"] >= 0) &
    (df["p"] >= 0) &
    (df["k"] >= 0) &
    (df["temperature"].between(0, 60)) &
    (df["humidity"].between(0, 100)) &
    (df["ph"].between(3, 10)) &
    (df["rainfall"] >= 0)
]

print("After cleaning:", df.shape)

# ==========================================
# STEP 5 — Encode target (crop label)
# ==========================================
label_encoder = LabelEncoder()
df["label"] = label_encoder.fit_transform(df["label"])

print("Number of crop classes:", len(label_encoder.classes_))

# ==========================================
# STEP 6 — Define features
# ==========================================
feature_columns = [
    "n","p","k",
    "temperature","humidity","ph","rainfall",
    "irrigation_type",
    "water_availability",
    "market_type",
    "market_distance"
]

X = df[feature_columns]
y = df["label"]

# save feature list for prediction consistency
joblib.dump(feature_columns, "model_features.pkl")

# ==========================================
# STEP 7 — Feature types
# ==========================================
numeric_features = [
    "n","p","k","temperature","humidity","ph","rainfall"
]

categorical_features = [
    "irrigation_type",
    "water_availability",
    "market_type",
    "market_distance"
]

# ==========================================
# STEP 8 — Preprocessing
# ==========================================
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

# ==========================================
# STEP 9 — Multi-class XGBoost Model
# ==========================================
xgb_model = XGBClassifier(
    n_estimators=500,           # stronger learning
    learning_rate=0.05,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="multi:softprob", # ⭐ important for multi-crop probabilities
    random_state=42,
    eval_metric="mlogloss"
)

# ==========================================
# STEP 10 — Build pipeline
# ==========================================
model_pipeline = Pipeline([
    ("preprocessing", preprocessor),
    ("classifier", xgb_model)
])

# ==========================================
# STEP 11 — Train-test split
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training samples:", X_train.shape)
print("Testing samples:", X_test.shape)

# ==========================================
# STEP 12 — Train model
# ==========================================
print("\nTraining model...")
model_pipeline.fit(X_train, y_train)
print("Training completed.")

# ==========================================
# STEP 13 — Evaluate model
# ==========================================
pred = model_pipeline.predict(X_test)

accuracy = accuracy_score(y_test, pred)
print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, pred))

# ==========================================
# STEP 14 — Save trained model
# ==========================================
joblib.dump(model_pipeline, "crop_model_pipeline.pkl")
joblib.dump(label_encoder, "crop_label_encoder.pkl")

print("\nModel saved successfully!")
print("Files saved:")
print("✔ crop_model_pipeline.pkl")
print("✔ crop_label_encoder.pkl")
print("✔ model_features.pkl")

print("\n========== PROCESS COMPLETED ==========")