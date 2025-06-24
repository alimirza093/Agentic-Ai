from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import os
import shutil

Upload_folder = "uploads"

os.makedirs(Upload_folder, exist_ok=True)
app = FastAPI()

app.mount("/uploads", StaticFiles(directory=Upload_folder), name="uploads")
@app.post("/uploadfile/")
async def upload_files(file : UploadFile = File(...)):
    if not file.filename:
        return {"error": "No file selected"}
    if not file.filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return {"error": "File type not allowed"}
    content = await file.read()
    if len(content) > 2 * 1024 * 1024:
        return {"error": "File size exceeds 2MB limit"}
    file_path = os.path.join(Upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_url = f"/uploads/{file.filename}"

    return {
        "data": {
            "filename": file.filename,
            "url": f"http://localhost:8000{file_url}"
        },
        "message": "File uploaded successfully",
        "status": "success"
    }