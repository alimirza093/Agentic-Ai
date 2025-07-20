from fastapi import FastAPI
from routers.todo_routers import todo_router
from routers.user_routers import user_router

app = FastAPI()

app.include_router(todo_router, prefix="/todo", tags=["Todo"])
app.include_router(user_router, prefix="/user", tags=["User"])
