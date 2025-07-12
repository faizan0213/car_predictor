from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

# 🔹 SQLModel for Database Table (Users Table)
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str  # Hashed password

# 🔹 Pydantic Models for API (Request/Response)

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
