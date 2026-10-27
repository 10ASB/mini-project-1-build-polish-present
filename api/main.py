from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path

app = FastAPI(
    title="Delivery Delay Prediction API",
    description="API for predicting delivery delays",
    version="1.0"
)

# Load model
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"

model = joblib.load(MODEL_PATH)
print("MODEL LOADED:", type(model))


class PredictionRequest(BaseModel):
    customer_city: str
    product_category: str
    product_weight_kg: float
    discount_pct: float
    courier_partner: str
    promised_delivery_days: int
    warehouse_zone: str
    payment_mode: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/predict")
def predict(request: PredictionRequest):
    data = pd.DataFrame([{
        "customer_city": request.customer_city,
        "product_category": request.product_category,
        "product_weight_kg": request.product_weight_kg,
        "discount_pct": request.discount_pct,
        "courier_partner": request.courier_partner,
        "promised_delivery_days": request.promised_delivery_days,
        "warehouse_zone": request.warehouse_zone,
        "payment_mode": request.payment_mode
    }])

    prediction = model.predict(data)[0]

    return {
        "prediction": int(prediction),
        "is_delayed": bool(prediction)
    }
