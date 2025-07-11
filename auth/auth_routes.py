from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import UserRegister, TokenResponse
from auth.hashing import hash_password, verify_password
from auth.jwt_handler import create_token, decode_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Temporary in-memory DB
users_db = {}

@router.post("/register")
def register(user: UserRegister):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = hash_password(user.password)
    return {"msg": "User registered successfully"}

@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends()):
    username = form.username
    password = form.password

    if username not in users_db or not verify_password(password, users_db[username]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user": payload.get("sub")}

@router.get("/predict")
def predict(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    return {"msg": f"Prediction allowed for user {payload['sub']}"}
