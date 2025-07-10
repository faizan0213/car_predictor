from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load model and encoders
model = joblib.load('car_price_model.pkl')
le_fuel = joblib.load('le_fuel.pkl')
le_transmission = joblib.load('le_transmission.pkl')
le_owner = joblib.load('le_owner.pkl')
le_brand = joblib.load('le_brand.pkl')
le_model = joblib.load('le_model.pkl')

# FastAPI app
app = FastAPI()

# Request body model
class CarData(BaseModel):
    Year: int
    Age: int
    kmDriven: int
    FuelType: str
    Transmission: str
    Owner: str
    Brand: str
    model: str

@app.post("/predict")
def predict_price(data: CarData):
    # Clean and encode input
    fuel = data.FuelType.strip().title()
    trans = data.Transmission.strip().title()
    owner = data.Owner.strip().lower()
    brand = data.Brand.strip()
    model_name = data.model.strip()

    try:
        encoded_input = np.array([
            data.Year,
            data.Age,
            data.kmDriven,
            le_fuel.transform([fuel])[0],
            le_transmission.transform([trans])[0],
            le_owner.transform([owner])[0],
            le_brand.transform([brand])[0],
            le_model.transform([model_name])[0]
        ]).reshape(1, -1)

        prediction = model.predict(encoded_input)[0]
        return {"predicted_price": round(prediction, 2)}

    except Exception as e:
        return {"error": f"Invalid input: {e}"}
