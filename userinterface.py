import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------------------------------
# USER CONFIG
# -------------------------------------------------
MODEL_FILENAME = "best_model_LinearRegression.joblib"
BACKGROUND_PATH_OR_URL = "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1650&q=80"
APP_TITLE = "🌾 AgriYield Predictor"
# -------------------------------------------------

st.set_page_config(page_title="AgriYield Predictor", layout="wide", page_icon="🌾")

# -------------------------------------------------
# BACKGROUND CSS
# -------------------------------------------------
def set_background(image_url):
    css = f"""
    <style>
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.14), rgba(255,255,255,0.14)),
                        url("{image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .content-box {{
            background: rgba(255,255,255,0.92);
            padding: 18px;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        }}
        .card {{
            background: white;
            padding: 14px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        .small-muted {{
            font-size: 12px;
            color: #6b6b6b;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background(BACKGROUND_PATH_OR_URL)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown(
    f"""
    <div style="margin-bottom:15px;">
      <div class="card">
        <h1 style="color:#0b5f2b; margin-bottom:4px;">{APP_TITLE}</h1>
        <p class="small-muted">Predict accurate crop yield using soil and environmental features</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# LOAD MODEL SAFELY
# -------------------------------------------------
@st.cache_resource
def load_model():
    if os.path.exists(MODEL_FILENAME):
        try:
            model = joblib.load(MODEL_FILENAME)
            return model
        except Exception:
            st.error("❌ Could not load model. Please re-upload the .joblib file.")
            return None
    else:
        st.warning(f"⚠️ Model file '{MODEL_FILENAME}' not found. Using demo baseline model.")
        class DemoModel:
            def predict(self, X):
                return np.full(len(X), 2.5)
        return DemoModel()

model = load_model()

# -------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------
with st.sidebar:
    st.header("⚙️ Options")

    preset = st.selectbox("Select sample preset:", [
        "None",
        "Wheat - Kharif - Loam",
        "Rice - Kharif - Clay",
        "Maize - Rabi - Sandy"
    ])

    st.write("---")
    st.subheader("📤 Batch CSV Upload")
    csv_file = st.file_uploader("Upload CSV", type=["csv"])

# Preset values
PRESETS = {
    "Wheat - Kharif - Loam": {"N":100, "P":50, "K":30, "temperature":25, "humidity":60, "ph":6.5, "rainfall":50},
    "Rice - Kharif - Clay": {"N":140, "P":60, "K":40, "temperature":28, "humidity":75, "ph":6.2, "rainfall":120},
    "Maize - Rabi - Sandy": {"N":80, "P":40, "K":25, "temperature":22, "humidity":55, "ph":6.8, "rainfall":35}
}

# -------------------------------------------------
# INPUT FORM
# -------------------------------------------------
st.markdown("<div class='content-box'>", unsafe_allow_html=True)
st.subheader("🧪 Single Prediction")

if preset != "None":
    default = PRESETS[preset]
else:
    default = {"N":100, "P":50, "K":30, "temperature":25, "humidity":60, "ph":6.5, "rainfall":50}

col1, col2, col3 = st.columns(3)

with col1:
    N = st.number_input("Nitrogen (N)", value=float(default["N"]))
    P = st.number_input("Phosphorus (P)", value=float(default["P"]))
    K = st.number_input("Potassium (K)", value=float(default["K"]))

with col2:
    temperature = st.number_input("Temperature (°C)", value=float(default["temperature"]))
    humidity = st.number_input("Humidity (%)", value=float(default["humidity"]))
    ph = st.number_input("Soil pH", value=float(default["ph"]))

with col3:
    rainfall = st.number_input("Rainfall (mm)", value=float(default["rainfall"]))
    crop = st.text_input("Crop", value="")
    season = st.text_input("Season", value="")
    soil_type = st.text_input("Soil Type", value="")

input_data = pd.DataFrame([{
    "N": N, "P": P, "K": K,
    "temperature": temperature,
    "humidity": humidity,
    "ph": ph,
    "rainfall": rainfall,
    "Crop": crop,
    "Season": season,
    "Soil_Type": soil_type
}])

if st.button("🔮 Predict"):
    try:
        pred = model.predict(input_data)[0]
        st.markdown(
            f"""
            <div class="card">
              <h2>Predicted Yield: <span style="color:#0b5f2b">{pred:.3f} t/ha</span></h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f"Prediction failed: {e}")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# BATCH PREDICTION
# -------------------------------------------------
st.markdown("<div class='content-box' style='margin-top:15px;'>", unsafe_allow_html=True)
st.subheader("📈 Batch Prediction (CSV)")

if csv_file:
    try:
        df = pd.read_csv(csv_file)
        st.write("Preview:", df.head())
        preds = model.predict(df)
        df["Predicted_Yield"] = preds
        st.success("Batch prediction complete!")
        st.dataframe(df)

        st.download_button(
            label="Download Predictions CSV",
            data=df.to_csv(index=False).encode(),
            file_name="batch_predictions.csv",
        )
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Upload a CSV file to run batch predictions.")

st.markdown("</div>", unsafe_allow_html=True)
