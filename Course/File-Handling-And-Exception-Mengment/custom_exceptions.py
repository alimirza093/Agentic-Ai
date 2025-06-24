from fastapi.responses import JSONResponse
from fastapi import HTTPException , FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi import Request
from pydantic import BaseModel , EmailStr
from typing import Optional
app = FastAPI()

class Student(BaseModel):
    email : EmailStr
    phone_number : str
    address : str
    addmission_number : int
    age : int
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "error": error['msg'],
            "field": ".".join(map(str, error['loc']))
        })
    return JSONResponse(
        status_code=422,
        content={
            "errors": errors,
            "message": "Validation error",
            "status": "error"
        }
    )
@app.get("/")
async def root():
    return {"message": "Welcome to the Student Registration API"}

@app.post("/student/{student_id}")
async def register_student(student_id: int, student: Student , name:str , semester:Optional[str]):
        if not student.phone_number.isdigit():
            raise HTTPException(status_code=422, detail="Phone number must be numeric")
        if len(student.phone_number) != 11:
            raise HTTPException(status_code=422, detail="Phone number must be 11 digits")
        if not student.email:
            raise HTTPException(status_code=422, detail="Email is required")
        if not student.address:
            raise HTTPException(status_code=422, detail="Address is required")
        if student.age < 18 or student.age > 30:
            raise HTTPException(status_code=422, detail="Age must be between 18 and 30")
        if not student.addmission_number:
            raise HTTPException(status_code=422, detail="Admission number is required")
        if not(student_id >= 500 and student_id <= 561):
            raise HTTPException(status_code=422, detail="Student ID must be between 500 and 561")

        return {
            "data": {
                "student_id": student_id,
                "name": name,
                "age": student.age,
                "semester": semester,
                "email": student.email,
                "phone_number": student.phone_number,
                "address": student.address,
                "addmission_number": student.addmission_number
            },
            "message": "Student registered successfully",
            "status": "success"
        }

