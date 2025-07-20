from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends , HTTPException
from fastapi.security import OAuth2PasswordBearer , APIKeyHeader
from config.db import get_db
from models.model import ApiKeyModel
import jwt
import secrets
import os


load_dotenv()

oAuth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

def verify_token(token: str = Depends(oAuth2_scheme)):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def generate_api_key():
    return secrets.token_hex(32)  # 64-character secure random string

def verify_api_key(api_key: str = Depends(api_key_header), db=Depends(get_db)):
    if not api_key:
        raise HTTPException(status_code=403, detail="API key is missing")
    
    existing_api_key = db.query(ApiKeyModel).filter(ApiKeyModel.key == api_key).first()
    if not existing_api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    