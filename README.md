# 🚗 Car Price Prediction API using FastAPI

This project is a **machine learning-powered API** built with **FastAPI** that predicts the price of a used car based on key features such as brand, model, year, kilometers driven, fuel type, transmission, and ownership.

---

## 📌 Features

- 🔮 Predicts car resale price using trained ML model
- ⚡ Fast and lightweight API using FastAPI
- 🎯 Clean data preprocessing and label encoding
- 🔗 Ready for Flutter or frontend integration
- ☁️ Easily deployable on Railway, Render, EC2, etc.

---

## 📊 Model Details

- Trained on: Indian used car dataset  
- Algorithm: Linear Regression  
- Libraries used: `scikit-learn`, `pandas`, `numpy`, `joblib`

---

## 🧠 Input Parameters (via JSON)

```json
{
  "Year": 2019,
  "Age": 5,
  "kmDriven": 42000,
  "FuelType": "Petrol",
  "Transmission": "Manual",
  "Owner": "first",
  "Brand": "Hyundai",
  "model": "Elite i20"
}

# Clone repo
git clone https://github.com/faizan0213/car_predictor.git
cd car_predictor

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI app
uvicorn main:app --reload


🧑‍💻 Author
Faizan
Flutter & Node.js Developer | Learning AI & Cloud ☁️
GitHub

