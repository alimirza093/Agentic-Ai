from fastapi import APIRouter, Depends, HTTPException
from config.db import get_db
from sqlalchemy.orm import Session, joinedload
from models.models import Todo
from pydantic import BaseModel, EmailStr
from utlis.helping_utils import verify_token
todo_router = APIRouter()


class create_Todo(BaseModel):
    title: str
    description: str
    completed: bool

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


@todo_router.post("/post")
def create_todo(todo: create_Todo, user = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        user_id = user.get("user_id")
        new_todo = Todo(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            user_id=user_id
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

@todo_router.get("/get")
def get_todos(user = Depends(verify_token) ,db: Session = Depends(get_db)):
    try:
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        todos = db.query(Todo).all()
        return{
            "message": "Todos retrieved successfully",
            "data": todos,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@todo_router.get("/get/{id}")
def get_todo_by_id(id: int, user = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
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
    
@todo_router.put("/update/{id}")
def update_todo(id: int , todo: create_Todo ,user = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
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
            

@todo_router.delete("/todos/delete/{id}")
def delete_todo(id: int,user = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
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