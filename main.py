from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.security import OAuth2PasswordBearer
from auth.auth_routes import router as AuthRouter
from auth.jwt_handler import decode_token


from fastapi.middleware.cors import CORSMiddleware


# Load model and encoders
model = joblib.load('car_price_model.pkl')
le_fuel = joblib.load('le_fuel.pkl')
le_transmission = joblib.load('le_transmission.pkl')
le_owner = joblib.load('le_owner.pkl')
le_brand = joblib.load('le_brand.pkl')
le_model = joblib.load('le_model.pkl')


# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, later replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRouter)  # 🔐 Register/login/me routes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # 🔐 For token extraction

# ✅ Input model
class CarData(BaseModel):
    Year: int
    Age: int
    kmDriven: int
    FuelType: str
    Transmission: str
    Owner: str
    Brand: str
    model: str

# ✅ JWT token validation
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

# 🔐 Protected Prediction Route
@app.post("/predict")
def predict_price(data: CarData, user=Depends(get_current_user)):
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
        return {
            "user": user["sub"],  # who's making prediction
            "predicted_price": round(prediction, 2)
        }

    except Exception as e:
        return {"error": f"Invalid input: {e}"}
