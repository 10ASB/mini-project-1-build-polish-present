import streamlit as st
import requests
import pandas as pd
from pathlib import Path

st.title("Delivery Delay Prediction")
st.write("Enter delivery details to predict whether the order will be delayed.")

# Load dataset to populate dropdown values
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "internB_delivery_delays_processed.csv"
df = pd.read_csv(DATA_PATH)

customer_cities = sorted(df["customer_city"].dropna().astype(str).unique().tolist())
product_categories = sorted(df["product_category"].dropna().astype(str).unique().tolist())
courier_partners = sorted(df["courier_partner"].dropna().astype(str).unique().tolist())
warehouse_zones = sorted(df["warehouse_zone"].dropna().astype(str).unique().tolist())
payment_modes = sorted(df["payment_mode"].dropna().astype(str).unique().tolist())

customer_city = st.selectbox("Customer City", customer_cities)
product_category = st.selectbox("Product Category", product_categories)
courier_partner = st.selectbox("Courier Partner", courier_partners)
warehouse_zone = st.selectbox("Warehouse Zone", warehouse_zones)
payment_mode = st.selectbox("Payment Mode", payment_modes)

product_weight_kg = st.number_input("Product Weight (kg)", min_value=0.0, value=1.0)
discount_pct = st.number_input("Discount (%)", min_value=0.0, value=10.0)
promised_delivery_days = st.number_input("Promised Delivery Days", min_value=1, value=3, step=1)

if st.button("Predict"):
    data = {
        "customer_city": customer_city,
        "product_category": product_category,
        "product_weight_kg": product_weight_kg,
        "discount_pct": discount_pct,
        "courier_partner": courier_partner,
        "promised_delivery_days": promised_delivery_days,
        "warehouse_zone": warehouse_zone,
        "payment_mode": payment_mode
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=data, timeout=30)
        result = response.json()

        if "error" in result:
            st.error(
                f"⚠️ {result['error']}\n\n"
                f"Field: {result.get('field', 'unknown')}\n"
                f"Value: {result.get('value', 'unknown')}"
            )
        elif response.status_code == 200:
            if result["is_delayed"]:
                st.error("⚠️ Delivery is likely to be delayed")
            else:
                st.success("✅ Delivery is not likely to be delayed")
            st.write("Prediction:", result["prediction"])
        else:
            st.error("API request failed.")
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to FastAPI. Make sure the API server is running.")
    except requests.exceptions.RequestException as exc:
        st.error(f"API request failed: {exc}")
