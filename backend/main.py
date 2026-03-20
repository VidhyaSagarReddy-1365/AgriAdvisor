# ============================================
# AgriAdvisor - FastAPI Backend
# main.py
# ============================================

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Union
from dotenv import load_dotenv
import pandas as pd
import joblib
import pickle
import os
import traceback

load_dotenv()

from auth import (
    hash_password, verify_password,
    create_token, decode_token,
    get_current_user
)
from database import (
    create_user, get_user_by_email,
    save_prediction, get_user_predictions
)

# ============================================
# APP SETUP
# ============================================

app = FastAPI(title="AgriAdvisor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# LOAD ML MODELS AT STARTUP
# ============================================

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

print("Loading XGBoost model...")
crop_model    = joblib.load(os.path.join(MODEL_DIR, "crop_model_pipeline.pkl"))
label_encoder = joblib.load(os.path.join(MODEL_DIR, "crop_label_encoder.pkl"))
print("XGBoost model loaded!")


def load_prophet(crop_name: str):
    """Load a Prophet model for a given crop."""
    # Capitalize to match filenames: Rice_prophet.pkl
    crop_name = crop_name.strip().capitalize()
    path = os.path.join(MODEL_DIR, "prophet_models", f"{crop_name}_prophet.pkl")
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


def predict_price(crop_name: str):
    """Use Prophet to forecast price 30 days out."""
    model = load_prophet(crop_name)
    if model is None:
        return "N/A"
    try:
        future   = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        price    = forecast["yhat"].iloc[-1]
        return round(float(price), 2)
    except Exception:
        return "N/A"


# ============================================
# REQUEST SCHEMAS
# ============================================

class PredictRequest(BaseModel):
    n:                  float
    p:                  float
    k:                  float
    temperature:        float
    humidity:           float
    ph:                 float
    rainfall:           float
    irrigation_type:    str
    water_availability: str
    market_type:        str
    market_distance:    str


class RegisterRequest(BaseModel):
    name:     str
    email:    str
    password: str
    answer1:  str
    answer2:  str


class LoginRequest(BaseModel):
    email:    str
    password: str


class ResetPasswordRequest(BaseModel):
    email:        str
    answer1:      str
    answer2:      str
    new_password: str


class ChangePasswordRequest(BaseModel):
    new_password: str


# ============================================
# PREDICTION LOGIC
# ============================================

def run_prediction(data: PredictRequest):

    # Soil suitability check
    if (
        data.n <= 5 and
        data.p <= 5 and
        data.k <= 5 and
        data.rainfall <= 5
    ):
        raise HTTPException(
            status_code=400,
            detail="Soil not suitable. Improve fertility and irrigation first."
        )

    if not (0 <= data.humidity <= 100):
        raise HTTPException(status_code=400, detail="Invalid humidity value.")

    if not (3 <= data.ph <= 10):
        raise HTTPException(status_code=400, detail="Invalid soil pH value.")

    # Build input dataframe
    input_dict = {
        "n":                  data.n,
        "p":                  data.p,
        "k":                  data.k,
        "temperature":        data.temperature,
        "humidity":           data.humidity,
        "ph":                 data.ph,
        "rainfall":           data.rainfall,
        "irrigation_type":    data.irrigation_type,
        "water_availability": data.water_availability.lower(),
        "market_type":        data.market_type,
        "market_distance":    data.market_distance,
    }
    input_df = pd.DataFrame([input_dict])

    # XGBoost prediction
    probs      = crop_model.predict_proba(input_df)[0]
    crop_names = label_encoder.classes_

    results = pd.DataFrame({
        "Crop":       crop_names,
        "Confidence": probs * 100
    }).sort_values("Confidence", ascending=False)

    # Water-based filter
    water = data.water_availability.lower()
    if water == "low":
        results = results[~results["Crop"].isin(["rice", "banana", "jute"])]
    elif water == "medium":
        results = results[~results["Crop"].isin(["rice"])]

    # Top 3 crops
    top3     = results.head(3)
    top_conf = top3.iloc[0]["Confidence"]

    # Advice
    if top_conf >= 60:
        advice = (
            f"Excellent conditions detected. "
            f"{top3.iloc[0]['Crop'].capitalize()} is strongly recommended "
            f"for your soil and climate profile."
        )
    elif top_conf >= 40:
        advice = (
            "Moderate conditions detected. "
            "Multiple crops can work — consider market demand and irrigation availability."
        )
    else:
        advice = (
            "Conditions are uncertain for profitable farming. "
            "Consider improving soil nutrients, irrigation, or consult a local agronomist."
        )

    # Build response
    top_crops = []
    for _, row in top3.iterrows():
        crop  = row["Crop"]
        conf  = round(float(row["Confidence"]), 2)
        price = predict_price(crop)
        top_crops.append({
            "name":       crop.capitalize(),
            "confidence": conf,
            "price":      price
        })

    return {
        "top_crops": top_crops,
        "advice":    advice
    }


# ============================================
# ROUTES
# ============================================

@app.get("/")
def root():
    return {"message": "AgriAdvisor API is running"}


# --- Register ---
@app.post("/register")
def register(req: RegisterRequest):
    try:
        existing = get_user_by_email(req.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered.")

        create_user({
            "name":     req.name,
            "email":    req.email,
            "password": hash_password(req.password),
            "answer1":  req.answer1.strip().lower(),
            "answer2":  req.answer2.strip().lower(),
        })
        return {"message": "Registration successful"}

    except HTTPException:
        raise
    except Exception as e:
        print("REGISTER ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# --- Login ---
@app.post("/login")
def login(req: LoginRequest):
    try:
        user = get_user_by_email(req.email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found.")

        if not verify_password(req.password, user["password"]):
            raise HTTPException(status_code=401, detail="Incorrect password.")

        token = create_token({"email": user["email"], "name": user["name"]})
        return {
            "token": token,
            "name":  user["name"],
            "email": user["email"]
        }

    except HTTPException:
        raise
    except Exception as e:
        print("LOGIN ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# --- Predict ---
@app.post("/predict")
def predict(
    request: PredictRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        result = run_prediction(request)
        save_prediction(
            user_email = current_user["email"],
            inputs     = request.dict(),
            result     = result
        )
        return result

    except HTTPException:
        raise
    except Exception as e:
        print("PREDICT ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# --- Reset Password ---
@app.post("/reset-password")
def reset_password(req: ResetPasswordRequest):
    try:
        user = get_user_by_email(req.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        if (
            user["answer1"] != req.answer1.strip().lower() or
            user["answer2"] != req.answer2.strip().lower()
        ):
            raise HTTPException(status_code=401, detail="Security answers incorrect.")

        from database import update_password
        update_password(req.email, hash_password(req.new_password))
        return {"message": "Password reset successful"}

    except HTTPException:
        raise
    except Exception as e:
        print("RESET ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# --- Change Password (authenticated) ---
@app.post("/change-password")
def change_password(
    req: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        from database import update_password
        update_password(current_user["email"], hash_password(req.new_password))
        return {"message": "Password changed successfully"}

    except Exception as e:
        print("CHANGE PASSWORD ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# --- History ---
@app.get("/history")
def history(current_user: dict = Depends(get_current_user)):
    try:
        records = get_user_predictions(current_user["email"])
        return {"history": records}

    except Exception as e:
        print("HISTORY ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# --- Profile ---
@app.get("/profile")
def profile(current_user: dict = Depends(get_current_user)):
    try:
        user = get_user_by_email(current_user["email"])
        return {
            "name":  user["name"],
            "email": user["email"]
        }

    except Exception as e:
        print("PROFILE ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))