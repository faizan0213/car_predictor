from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select

from models import User, TokenResponse, UserRegister
from auth.hashing import hash_password, verify_password
from auth.jwt_handler import create_token, decode_token
from database import get_session

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register")
def register(user: UserRegister, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User(username=user.username, password=hash_password(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"msg": "User registered successfully"}

@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    username = form.username
    password = form.password

    db_user = session.exec(select(User).where(User.username == username)).first()
    if not db_user or not verify_password(password, db_user.password):
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