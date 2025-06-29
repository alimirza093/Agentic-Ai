from fastapi import FastAPI , Depends , HTTPException
from sqlalchemy.orm import Session , joinedload
from config.db import get_db , SessionLocal , engine
from models.models import User, todos
from pydantic import BaseModel , EmailStr


app = FastAPI()

class user_Base(BaseModel):
    username: str
    email: EmailStr
    password: str

class todo_Base(BaseModel):
    title: str
    description: str
    owner_id: int


class user_Response(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class todo_Response(BaseModel):
    id: int
    title: str
    description: str
    owner: user_Response
    class Config:
        orm_mode = True

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API!"}

@app.post("/todos" , response_model=todo_Response)
def create_todo(todo: todo_Base, db: Session = Depends(get_db)):
    try:
        db_todo = todos(title=todo.title, description=todo.description, owner_id=todo.owner_id)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/users")
def create_user(user: user_Base, db: Session = Depends(get_db)):
    try:
        db_user = User(username=user.username, email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/todos/{todo_id}")
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    full_todo = db.query(todos).options(joinedload(todos.owner)).filter(todos.id == todo_id).first()
    if not full_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return full_todo