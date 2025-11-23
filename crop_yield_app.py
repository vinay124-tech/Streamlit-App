# Crop Yield Prediction - Streamlit App
# Created for deployment on Streamlit Cloud
# Author: Manohar Vinay Mududundi

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import base64

# ---------- USER CONFIG ----------
# Update this path to your model file location
MODEL_PATH = "final_best_model.joblib"
BACKGROUND_PATH_OR_URL = "https://wallpaperaccess.com/full/736046.jpg"
# ---------------------------------

# Page configuration
st.set_page_config(
    page_title="Crop Yield Predictor", 
    layout="wide", 
    page_icon="🌾",
    initial_sidebar_state="collapsed"
)

# ---------- BACKGROUND IMAGE ----------
def set_background(image_path_or_url, overlay_rgba="rgba(255,255,255,0.15)"):
    """Sets page background with optional overlay"""
    try:
        if image_path_or_url.startswith("http"):
            css = f"""
            <style>
            .stApp {{
              background: linear-gradient({overlay_rgba},{overlay_rgba}), url("{image_path_or_url}");
              background-size: cover;
              background-position: center;
              background-attachment: fixed;
            }}
            .content-box {{
              background: rgba(255,255,255,0.85);
              padding: 20px;
              border-radius: 10px;
              box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }}
            </style>
            """
            st.markdown(css, unsafe_allow_html=True)
            return True
        elif os.path.exists(image_path_or_url):
            with open(image_path_or_url, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            css = f"""
            <style>
            .stApp {{
              background: linear-gradient({overlay_rgba},{overlay_rgba}), url("data:image/jpg;base64,{b64}");
              background-size: cover;
              background-position: center;
              background-attachment: fixed;
            }}
            .content-box {{
              background: rgba(255,255,255,0.85);
              padding: 20px;
              border-radius: 10px;
              box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }}
            </style>
            """
            st.markdown(css, unsafe_allow_html=True)
            return True
    except Exception as e:
        st.warning(f"Background image failed: {e}")
    return False

set_background(BACKGROUND_PATH_OR_URL)

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model(path):
    """Load the trained model with caching"""
    if not os.path.exists(path):
        return None, f"Model not found at {path}"
    try:
        return joblib.load(path), None
    except Exception as e:
        return None, str(e)

model, err = load_model(MODEL_PATH)
if model is None:
    st.error(f"❌ Model could not be loaded: {err}")
    st.info("💡 Please ensure 'best_model_LinearRegression.joblib' is in the same directory as this app.")
    st.stop()

# ---------- HEADER ----------
st.markdown("""
    <div style="background-color:white; border-radius:10px; padding:15px; box-shadow:0 2px 8px rgba(0,0,0,0.15); text-align:center; margin-bottom:10px;">
        <h1 style="color:#0b5f2b; font-weight:700; margin:0;">🌾 Crop Yield Predictor</h1>
        <p style="color:#2e2e2e; font-size:16px; margin-top:4px;">
            Enter your crop and soil parameters to estimate yield instantly.
        </p>
    </div>
""", unsafe_allow_html=True)

# ---------- INPUT FORM ----------
st.markdown("<div class='content-box'>", unsafe_allow_html=True)
st.subheader("📊 Input Parameters")

# Define feature lists - adjust these based on your model's requirements
numeric_features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
categorical_features = ["Crop", "Season", "Soil_Type"]

# Initialize session state for inputs
if "inputs" not in st.session_state:
    st.session_state.inputs = {}

inputs = {}

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Soil & Environmental Parameters**")
    inputs["N"] = st.number_input("Nitrogen (N) - kg/ha", value=0.0, step=1.0, format="%.2f", help="Amount of Nitrogen in soil")
    inputs["P"] = st.number_input("Phosphorus (P) - kg/ha", value=0.0, step=1.0, format="%.2f", help="Amount of Phosphorus in soil")
    inputs["K"] = st.number_input("Potassium (K) - kg/ha", value=0.0, step=1.0, format="%.2f", help="Amount of Potassium in soil")
    inputs["temperature"] = st.number_input("Temperature (°C)", value=25.0, step=0.1, format="%.2f", help="Average temperature")

with col2:
    st.markdown("**Additional Parameters**")
    inputs["humidity"] = st.number_input("Humidity (%)", value=50.0, min_value=0.0, max_value=100.0, step=1.0, format="%.2f", help="Relative humidity")
    inputs["ph"] = st.number_input("Soil pH", value=6.5, min_value=0.0, max_value=14.0, step=0.1, format="%.2f", help="Soil pH level")
    inputs["rainfall"] = st.number_input("Rainfall (mm)", value=100.0, step=1.0, format="%.2f", help="Annual rainfall")

# Categorical inputs
st.markdown("---")
st.markdown("**Crop Information**")
col3, col4, col5 = st.columns(3)

with col3:
    inputs["Crop"] = st.text_input("Crop Type", value="", placeholder="e.g., Rice, Wheat, Maize", help="Enter crop name")

with col4:
    inputs["Season"] = st.selectbox(
        "Season",
        options=["", "Kharif", "Rabi", "Zaid", "Whole Year"],
        help="Select growing season"
    )

with col5:
    inputs["Soil_Type"] = st.selectbox(
        "Soil Type",
        options=["", "Loamy", "Sandy", "Clayey", "Black", "Red", "Alluvial"],
        help="Select soil type"
    )

# Prediction button with custom styling
st.markdown("<br>", unsafe_allow_html=True)
predict_button = st.button("🔮 Predict Yield", use_container_width=True)

if predict_button:
    # Validate inputs
    missing_fields = []
    for key, value in inputs.items():
        if value == "" or (isinstance(value, (int, float)) and value == 0.0 and key in ["N", "P", "K"]):
            if key in categorical_features and value == "":
                missing_fields.append(key)

    if missing_fields:
        st.warning(f"⚠️ Please fill in the following fields: {', '.join(missing_fields)}")
    else:
        # Create dataframe for prediction
        sample = pd.DataFrame([inputs])

        try:
            # Make prediction
            pred = model.predict(sample)[0]

            # Display prediction with custom styling
            st.markdown(
                f"""<div style='text-align:center; margin-top:20px; padding:20px; 
                border-radius:10px; background:#eaffea; color:#0b5f2b; font-size:24px; 
                box-shadow: 0 4px 12px rgba(11,95,43,0.2);'>
                <b>🎯 Predicted Yield:</b> <span style='font-size:32px; font-weight:800;'>{pred:.3f}</span> t/ha
                </div>""",
                unsafe_allow_html=True,
            )

            # Store in history
            if "history" not in st.session_state:
                st.session_state["history"] = []

            rec = sample.copy()
            rec["Predicted_Yield"] = pred
            rec["Timestamp"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state["history"].append(rec)

            # Success message
            st.success("✅ Prediction completed successfully!")

        except Exception as e:
            st.error(f"⚠️ Prediction failed: {e}")
            st.info("Please check if all input values are valid and the model is compatible.")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- HISTORY SECTION ----------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='content-box'>", unsafe_allow_html=True)
st.subheader("📜 Prediction History")

if "history" in st.session_state and len(st.session_state["history"]) > 0:
    hist_df = pd.concat(st.session_state["history"], ignore_index=True)

    # Display statistics
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Total Predictions", len(hist_df))
    with col_stat2:
        st.metric("Average Yield", f"{hist_df['Predicted_Yield'].mean():.2f} t/ha")
    with col_stat3:
        st.metric("Max Yield", f"{hist_df['Predicted_Yield'].max():.2f} t/ha")

    # Show recent predictions
    st.markdown("**Recent Predictions:**")
    st.dataframe(hist_df.tail(10), use_container_width=True)

    # Download button
    csv = hist_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Full Prediction History (CSV)", 
        data=csv, 
        file_name=f"yield_predictions_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

    # Clear history button
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state["history"] = []
        st.rerun()
else:
    st.info("📝 No predictions yet. Enter parameters above and click 'Predict Yield' to get started!")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
    <hr style="opacity:0.3;">
    <p style="text-align:center; color:white; font-size:13px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
    Designed by <b>Manohar Vinay Mududundi</b> | Crop Yield Prediction UI 2025
    </p>
""", unsafe_allow_html=True)

# ---------- SIDEBAR (Optional) ----------
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.info("""
    This application predicts crop yield based on:
    - Soil nutrients (N, P, K)
    - Environmental factors (temperature, humidity, rainfall)
    - Soil properties (pH, type)
    - Crop and season information

    **Model**: Linear Regression
    """)

    st.markdown("### 📖 Instructions")
    st.markdown("""
    1. Enter soil nutrient values
    2. Provide environmental parameters
    3. Select crop, season, and soil type
    4. Click 'Predict Yield'
    5. View and download prediction history
    """)

    st.markdown("---")
    st.markdown("**Version**: 1.0")
    st.markdown("**Last Updated**: November 2025")
