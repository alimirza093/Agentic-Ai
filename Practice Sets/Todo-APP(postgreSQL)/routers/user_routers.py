from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import User
from pydantic import BaseModel, EmailStr
from config.db import get_db
from utlis.helping_utils import create_access_token

user_router = APIRouter()

class create_User(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class login_User(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


@user_router.post("/signup")
def create_user(user: create_User, db: Session = Depends(get_db)):
    try:
        new_user = User(
            username=user.username,
            email=user.email,
            password=user.password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User creation failed")
        Token = create_access_token(data={"user_id": db_user.id , "email": db_user.email , "username": db_user.username})
        return {
            "message": "User created successfully",
            "token": Token,
            "status": "success"
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error creating user",
            "error": str(e),
            "status": "error"
        }

@user_router.post("/login")
def login_user(user: login_User, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="User not found")
        if db_user.password != user.password: # type: ignore
            raise HTTPException(status_code=400, detail="Incorrect password")
        
        Token = create_access_token(data={"user_id": db_user.id , "email": db_user.email , "username": db_user.username})

        return {
            "message": "Login successful",
            "token": Token,
            "status": "success"
        }
    except Exception as e:
        return {
            "message": "Error logging in",
            "error": str(e),
            "status": "error"
        }