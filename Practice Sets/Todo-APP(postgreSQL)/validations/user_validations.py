from pydantic import BaseModel, EmailStr

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