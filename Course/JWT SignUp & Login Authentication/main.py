from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI , Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import User
from config.Database import get_db
import jwt
from dotenv import load_dotenv
import os
from pydantic import BaseModel , EmailStr

class User_login(BaseModel):
    email: EmailStr
    password: str

class registerUser(BaseModel):
    email: EmailStr
    password: str
    username: str

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

app = FastAPI()

@app.post("/user/login")
def login(user : User_login , db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or user.password != db_user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return{
        "user_data" : {
            "email": db_user.email,
            "username": db_user.username
        },
        "access_token": access_token
    }

@app.post("/user/register")
def register(user: registerUser, db: Session = Depends(get_db)):
    try:
        new_user = User(email=user.email, password=user.password , username=user.username)
        # Check if the user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {"message": "User registered successfully", "data" : new_user , "status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error registering user: {str(e)}",
        )