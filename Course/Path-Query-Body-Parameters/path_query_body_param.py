from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
class Person(BaseModel):
    name : str
    age : int
    email : str
    id : int

@app.get("/user/{user_id}/{name}")
def read_item(user_id: int, name: str, query: str):
    try:
        return {
            "message": "Data fetched successfully",

            "status": "Success",
            "Query" : query,

            "Data" : {
                "name": name,
                "age": 25,
                "email" : "ali8751805@gmail.com",
                "id" : user_id,
                }


                }
    except Exception as e:
        return {
            "message": str(e),
            "status": "Error",
            "Data" : None
        }
    
    #Body Perameters
@app.post("/user")
def create_user(user: Person):
    try:
        return {
            "message": "Data created successfully",
            "status": "Success",
            "Data" : user
        }
    except Exception as e:
        return {
            "message": str(e),
            "status": "Error",
            "Data" : None
        }
    
    
