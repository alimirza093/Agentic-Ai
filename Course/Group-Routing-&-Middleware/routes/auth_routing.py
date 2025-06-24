from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.get("/login")
async def login():
    return {"message": "Login successfully",
            "data": [
                {"id": 1, "username": "user1"},
                {"id": 2, "username": "user2"},
                {"id": 3, "username": "user3"},
            ],
            "status": "success"
}

@auth_router.post("/register")
async def register():
    return {"message": "Register successfully",
            "data": [
                {"id": 1, "username": "user1"},
                {"id": 2, "username": "user2"},
                {"id": 3, "username": "user3"},
            ],
            "status": "success"
}

@auth_router.post("/forget_password") 
async def forget_password():
    return {"message": "Forget password successfully",
            "data": [
                {"id": 1, "username": "user1"},
                {"id": 2, "username": "user2"},
                {"id": 3, "username": "user3"},
            ],
            "status": "success"
}