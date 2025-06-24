# Crud Operation in fastapi

import datetime
from fastapi import FastAPI , Request
from pymongo import MongoClient
from fastapi.responses import HTMLResponse
from datetime import datetime
from fastapi.responses import JSONResponse 
from pydantic import BaseModel
from bson import ObjectId


app = FastAPI()

class NoteEntity(BaseModel):
    note: str

try:
    conn = MongoClient("mongodb+srv://ali093:ali78585@firstcluster.pmz7w.mongodb.net/")
    print("No error Database connection failed")
except Exception as e:
    print("error Database connection failed")

@app.post("/")

async def create_notes(note : NoteEntity):
    if note == "":
        return {"error": "Note is empty"}
    # adding date to the note
    notee = {"note": note.note}
    notee["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    conn.notes.notes.insert_one(notee)
    return {"Message": "Note has been created successfully"}



@app.get("/")

def read_item(request: Request):
    docs = conn.notes.notes.find({})
    new_docs = []
    for doc in docs:
        date = doc.get("date", "No date available")
        new_docs.append(
            {
                "note": str(doc["note"]),
                "id": str(doc["_id"]),
                "date" : date
            }
        )
    return JSONResponse(content= new_docs)

@app.delete("/delete/{note_id}")
async def delete_notes(note_id: str):
    note = conn.notes.notes.find_one({"_id": ObjectId(note_id)})
    if note:
        conn.notes.notes.delete_one({"_id": ObjectId(note_id)})
        return {"Message": "Note has been deleted successfully"}
    else:
        return {"error": "Note not found"}
    
@app.put("/update/{note_id}")

async def update_notes(note_id: str, note: NoteEntity):
    notess = conn.notes.notes.find_one({"_id": ObjectId(note_id)})
    if notess:
        conn.notes.notes.update_one({"_id" : ObjectId(note_id)}, {"$set": {"note": note.note}})
        return {"Message": "Note has been updated successfully"}
    else:
        return {"error": "Note not found"}
    