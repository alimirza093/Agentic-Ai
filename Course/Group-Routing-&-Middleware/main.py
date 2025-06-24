from fastapi import FastAPI
from routes.auth_routing import auth_router
from routes.post_routing import post_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.2:9000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(post_router, prefix="/post", tags=["post"])
@app.get("/")
async def root():
    return {
        "message": "Server is running"
    }
