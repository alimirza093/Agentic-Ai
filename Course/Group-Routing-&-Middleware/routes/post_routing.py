from fastapi import APIRouter
from utlities.post_utilities import create_pdf , remove_pdf , update_pdf , get_pdf

post_router = APIRouter()

@post_router.get("/get")
async def get_post():
    return {"message": "Post get successfully",
            "data": [
                {"id": 1, "title": "Post 1"},
                {"id": 2, "title": "Post 2"},
                {"id": 3, "title": "Post 3"},
            ],
            "status": "success"
}


@post_router.post("/update")
async def update_post():
    return {"message": "Post updated successfully",
            "data": [
                {"id": 1, "title": "Post 1"},
                {"id": 2, "title": "Post 2"},
                {"id": 3, "title": "Post 3"},
            ],
            "status": "success"
}
            
@post_router.post("/create")
async def create_post():
    return {"message": "Post created successfully",
            "data": [
                {"id": 1, "title": "Post 1"},
                {"id": 2, "title": "Post 2"},
                {"id": 3, "title": "Post 3"},
            ],
            "status": "success"
}
@post_router.delete("/delete")
async def delete_post():
    return {"message": "Post deleted successfully",
            "data": [
                {"id": 1, "title": "Post 1"},
                {"id": 2, "title": "Post 2"},
                {"id": 3, "title": "Post 3"},
            ],
            "status": "success"
}            

@post_router.post("/create_pdf")
async def create_pdf_route():
    return create_pdf()

@post_router.delete("/remove_pdf")
async def remove_pdf_route():
    return remove_pdf()

@post_router.get("/get_pdf")
async def get_pdf_route():
    return get_pdf()

@post_router.put("/update_pdf")
async def update_pdf_route():
    return update_pdf()


