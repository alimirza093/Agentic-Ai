from fastapi import APIRouter, Depends, HTTPException
from config.db import get_db
from utlis.helping_utils import verify_token , generate_api_key
from models.model import ApiKeyModel

api_key_router = APIRouter()

@api_key_router.post("/get_api_key")
def get_api_key(user = Depends(verify_token), db=Depends(get_db)):
    try:
        user_id = user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        
        existing_api_key = db.query(ApiKeyModel).filter(ApiKeyModel.user_id == user_id).first()
        if existing_api_key:
            return {
                "message": "API key already exists",
                "data": {"api_key": existing_api_key.key},
                "status": "success"
            }
        
        new_api_key = ApiKeyModel(user_id=user_id, key=generate_api_key())
        db.add(new_api_key)
        db.commit()
        db.refresh(new_api_key)
        
        return {
            "message": "API key generated successfully",
            "data": {"api_key": new_api_key.key},
            "status": "success"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
