from pydantic import BaseModel

class create_Todo(BaseModel):
    title: str
    description: str
    completed: bool
