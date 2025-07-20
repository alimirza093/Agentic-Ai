from fastapi import APIRouter, Depends, HTTPException
from config.db import get_db
from utlis.helping_utils import create_access_token , verify_api_key
from models.model import User
from validations.user_validations import UserSignup, UserLogin


user_routes = APIRouter()

@user_routes.post("/signup")
def signup(user: UserSignup, db=Depends(get_db)):
    try:

        existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already exists")
        
        new_user = User(username=user.username, email=user.email, password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        token = create_access_token(data={"user_id": new_user.id, "username": new_user.username})
        return {
            "message": "User created successfully",
            "data": {
            "username": new_user.username,
            "email": new_user.email
        }, 
        "token": token,
        "status": "success"
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error creating user",
            "data" : None,
            "error": str(e),
            "status": "error"
        }
    
@user_routes.post("/login")
def login(user: UserLogin, db=Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if not existing_user:
            raise HTTPException(status_code=400, detail="user not found")
        if existing_user.password != user.password:
            raise HTTPException(status_code=400, detail="Incorrect password")
        
        token = create_access_token(data={"user_id": existing_user.id, "username": existing_user.username})
        return {
            "message": "Login successful",
            "data": {
                "username": existing_user.username,
                "email": existing_user.email
            },
            "token": token,
            "status": "success"
        }
    except Exception as e:
        return {
            "message": "Error logging in",
            "data" : None,
            "error": str(e),
            "status": "error"
        }
    
@user_routes.get("/secret_data" , dependencies=[Depends(verify_api_key)])
def secret_data():
    return {
        "message": "This is secret data",
        "status": "success"
    }
