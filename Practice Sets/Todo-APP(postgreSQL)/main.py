from fastapi import FastAPI , Depends , HTTPException
from Config.db import engine , SessionLocal 
from sqlalchemy.orm import Session , joinedload
from Models.models import Todo , User
from typing import List
from pydantic import BaseModel , EmailStr

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class create_Todo(BaseModel):
    title: str
    description: str
    completed: bool
    user_id: int

    class Config:
        orm_mode = True

class create_User(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    user_id: int
    datetime: str
    user: UserResponse
    class Config:
        orm_mode = True

@app.post("/todos/post")
def create_todo(todo: create_Todo, db: Session = Depends(get_db)):
    try:
        new_todo = Todo(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            user_id=todo.user_id
        )
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return {
            "message": "Todo created successfully",
            "data" : new_todo,
            "status": "success"
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error creating todo",
            "error": str(e),
            "status": "error"
        }

@app.post("/user/post")
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
        return {
            "message": "User created successfully",
            "data": new_user,
            "status": "success"
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error creating user",
            "error": str(e),
            "status": "error"
        }

@app.get("/todos/get")
def get_todos(db: Session = Depends(get_db)):
    try:
        todos = db.query(Todo).all()
        return{
            "message": "Todos retrieved successfully",
            "data": todos,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/todos/get/{id}")
def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    try:
        full_todo = db.query(Todo).options(joinedload(Todo.user)).filter(Todo.id == id).first()

        if not full_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {
            "message": "Todo retrieved successfully",
            "data": full_todo,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.put("/todos/update/{id}")
def update_todo(id: int, todo: create_Todo, db: Session = Depends(get_db)):
    try:
        existing_todo = db.query(Todo).filter(Todo.id == id).first()

        if not existing_todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        existing_todo.title = todo.title #type: ignore
        existing_todo.description = todo.description #type: ignore
        existing_todo.completed = todo.completed #type: ignore
        existing_todo.user_id = todo.user_id #type: ignore

        db.commit()
        db.refresh(existing_todo)

        return {
            "message": "Todo updated successfully",
            "data": existing_todo,
            "status": "success"
        }
    except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
            

@app.delete("/todos/delete/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    try:
        existing_todo = db.query(Todo).filter(Todo.id == id).first()

        if not existing_todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        db.delete(existing_todo)
        db.commit()

        return {
            "message": "Todo deleted successfully",
            "status": "success"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))