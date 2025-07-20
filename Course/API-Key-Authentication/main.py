from fastapi import FastAPI
from routes.user_routes import user_routes
from routes.api_key_route import api_key_router

app = FastAPI()
app.include_router(user_routes, prefix="/user", tags=["User Routes"])
app.include_router(api_key_router , prefix="/api_key", tags=["API Key Routes"])