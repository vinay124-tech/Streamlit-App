# Crop Yield Prediction - Streamlit App

A machine learning-based web application for predicting crop yields based on soil nutrients, environmental factors, and crop information.

## 📋 Features

- **Interactive UI**: Easy-to-use interface for inputting crop and soil parameters
- **Real-time Predictions**: Instant yield predictions using a trained Linear Regression model
- **Prediction History**: Track and download all your predictions
- **Responsive Design**: Works on desktop and mobile devices
- **Beautiful Background**: Custom agricultural-themed background image

## 🚀 Quick Start

### Local Deployment

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place your model file:**
   - Put your `best_model_LinearRegression.joblib` file in the same directory as `crop_yield_app.py`

3. **Run the app:**
   ```bash
   streamlit run crop_yield_app.py
   ```

4. **Access the app:**
   - Open your browser and go to `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Prepare your files:**
   - `crop_yield_app.py` (main app file)
   - `requirements.txt` (dependencies)
   - `best_model_LinearRegression.joblib` (your trained model)

2. **Upload to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

3. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select your repository
   - Set main file as `crop_yield_app.py`
   - Click "Deploy"

### Important Notes for Deployment

- **Model File**: Ensure `best_model_LinearRegression.joblib` is in the repository
- **File Size**: If model file is >100MB, use Git LFS or host it externally
- **Update MODEL_PATH**: In `crop_yield_app.py`, line 13, ensure MODEL_PATH points to your model file correctly

## 📊 Input Parameters

The app requires the following inputs:

### Numeric Features:
- **N**: Nitrogen content (kg/ha)
- **P**: Phosphorus content (kg/ha)
- **K**: Potassium content (kg/ha)
- **Temperature**: Average temperature (°C)
- **Humidity**: Relative humidity (%)
- **pH**: Soil pH level (0-14)
- **Rainfall**: Annual rainfall (mm)

### Categorical Features:
- **Crop**: Type of crop (e.g., Rice, Wheat, Maize)
- **Season**: Growing season (Kharif, Rabi, Zaid, Whole Year)
- **Soil_Type**: Type of soil (Loamy, Sandy, Clayey, Black, Red, Alluvial)

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **ML Model**: scikit-learn (Linear Regression)
- **Data Processing**: Pandas, NumPy
- **Model Persistence**: Joblib

## 📁 File Structure

```
project/
│
├── crop_yield_app.py          # Main Streamlit application
├── requirements.txt            # Python dependencies
├── best_model_LinearRegression.joblib  # Trained ML model
└── README.md                   # This file
```

## 🔧 Customization

### Change Background Image
Edit line 14 in `crop_yield_app.py`:
```python
BACKGROUND_PATH_OR_URL = "your-image-url-here"
```

### Modify Features
Update the feature lists in lines 115-116:
```python
numeric_features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
categorical_features = ["Crop", "Season", "Soil_Type"]
```

### Adjust Model Path
For different deployment environments, update line 13:
```python
MODEL_PATH = "path/to/your/model.joblib"
```

## 📝 Usage Example

1. Open the app
2. Enter soil nutrients (N, P, K values)
3. Input environmental parameters (temperature, humidity, rainfall)
4. Enter soil pH
5. Select crop type, season, and soil type
6. Click "🔮 Predict Yield"
7. View predicted yield in tons per hectare (t/ha)
8. Download prediction history as CSV

## ⚠️ Troubleshooting

**Model not loading:**
- Verify model file exists in the correct location
- Check MODEL_PATH variable matches your file location
- Ensure joblib version compatibility

**Background image not showing:**
- Check internet connection (for URL-based images)
- Verify image URL is accessible
- Try using a local image file instead

**Prediction errors:**
- Ensure all required fields are filled
- Check input values are within valid ranges
- Verify model was trained on the same features

## 👨‍💻 Author

**Manohar Vinay Mududundi**

M.Tech Student | Signal Processing & FPGA Implementation

## 📄 License

This project is created for educational and research purposes.

## 🤝 Contributing

Suggestions and improvements are welcome! Feel free to open issues or submit pull requests.

---

**Version**: 1.0  
**Last Updated**: November 2025
