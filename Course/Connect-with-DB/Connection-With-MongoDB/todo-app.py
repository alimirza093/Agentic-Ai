from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from datetime import datetime
app = FastAPI()

# MongoDB connection
try:
    client = MongoClient("mongodb+srv://ali093:ali51214@to-do-app.mydwfor.mongodb.net/")
    db = client["Todo-App"]
    collection = db["Todos"]
    print("MongoDB connection successful")
except Exception as e:
    print("MongoDB connection failed")
    print(e)



class Todo(BaseModel):
    title : str
    todo : str

@app.get("/")
def read_root():
    return {"message": "Server is running"}

@app.get("/todos")
def get_todos():
    try:
        todos = collection.find()
        todos_list = []
        for todo in todos:
            todos_list.append({
                "id": str(todo["_id"]),
                "title": todo["title"],
                "todo" : todo["todo"],
                "date": todo["date"]
            })
        return {
            "data": todos_list,
            "message": "Todos fetched successfully",
            "status": "success"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to fetch todos",
            "data" : []
        }

@app.get("/todos/{todo_id}")
def get_todo_by_id(todo_id: str):
    try:
        todo = collection.find_one({"_id": ObjectId(todo_id)})
        if todo:
            return {
                "data": {
                    "id": str(todo["_id"]),
                    "title": todo["title"],
                    "todo" : todo["todo"],
                    "date": todo["date"]
                },
                "message": "Todo fetched successfully",
                "status": "success"
            }
        else:
            return {
                "status": "error",
                "message": "Todo not found",
                "data" : []
            }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to fetch todo",
            "data" : [],
            "error": str(e)
        }

@app.get("/search")
def get_todo_by_title(todo_title: str):
    try:
        todo = collection.find_one({"title": todo_title})
        if todo:
            return {
                "data": {
                    "id": str(todo["_id"]),
                    "title": todo["title"],
                    "todo" : todo["todo"],
                    "date": todo["date"]
                },
                "message": "Todo fetched successfully",
                "status": "success"
            }
        else:
            return {
                "status": "error",
                "message": "Todo not found",
                "data" : []
            }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to fetch todo",
            "data" : [],
            "error": str(e)
        }


@app.post("/todos/post")
def create_todo(todo: Todo):
    try:
        if todo.todo == "" or todo.title == "":
            return {
                "status": "error",
                "message": "Todo is empty",
                "data" : []
            }
        todo_data = {
            "title": todo.title,
            "todo": todo.todo,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        collection.insert_one(todo_data)
        return {
            "status": "success",
            "message": "Todo created successfully",
            "data" : {
                "title": todo.title,
                "todo" : todo.todo,
                "date": todo_data["date"]
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to create todo",
            "data" : [],
            "error": str(e)
        }
    
@app.put("/todos/update/{todo_id}")
def update_todo(todo : Todo , todo_id : str):
    try:
        todo_data = collection.find_one({"_id": ObjectId(todo_id)})
        if not todo_data:
            return {
                "status": "error",
                "message": "Todo not found",
                "data" : []
            }
        todo_data = {
            "title": todo.title,
            "todo": todo.todo,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        collection.update_one({"_id": ObjectId(todo_id)}, {"$set": todo_data})
        return {
            "status": "success",
            "message": "Todo updated successfully",
            "data" : {
                "title": todo.title,
                "todo" : todo.todo,
                "date": todo_data["date"]
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to update todo",
            "data" : [],
            "error": str(e)
        }
    
@app.delete("/todos/delete/{todo_id}")
def delete_todo(todo_id: str):
    try:
        todo = collection.find_one({"_id": ObjectId(todo_id)})
        if todo:
            collection.delete_one({"_id": ObjectId(todo_id)})
            return {
                "status": "success",
                "message": "Todo deleted successfully",
                "data" : []
            }
        else:
            return {
                "status": "error",
                "message": "Todo not found",
                "data" : []
            }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to delete todo",
            "data" : [],
            "error": str(e)
        }

