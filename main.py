from typing import Dict, Optional

from fastapi import APIRouter, FastAPI
from pydantic import create_model

config = {
    "prefix": "/api",
    "routes": [
        {
            "tag": "Users",
            "url": "/users",
            "methods": ["GET", "POST"],
            "request_body": None,
            "response": {"id": (str, None), "name": (str, None)}
        },
        {
            "tag": "Posts",
            "url": "/posts",
            "methods": ["GET", "POST"],
            "request_body": {"title": (str, None), "content": (str, None)},
            "response": {"id": (str, None), "name": (str, None)}
        },
        {
            "tag": "Todos",
            "url": "/todos",
            "methods": ["GET", "PUT", "DELETE"],
            "request_body": {"title": (str, None), "content": (str, None)},
            "response": {"id": (str, None), "name": (str, None)}
        }
    ]
}

app = FastAPI()

def create_dynamic_model(model_name, fields: Dict[str, tuple]) -> type:
    """
    Create a dynamic Pydantic model based on the provided fields.
    """
    return create_model(model_name, **{
        field_name: (field_type, default_value)
        for field_name, (field_type, default_value) in fields.items()
    })

def create_router_from_config(config: Dict) -> APIRouter:
    # router = APIRouter(prefix="/apiv01")
    router = APIRouter(prefix=config["prefix"])

    def create_get_handler(url):
        async def get_handler():
            return {"message": f"GET request on {url}"}
        return get_handler

    def create_delete_handler(url):
        async def delete_handler():
            return {"message": f"DELETE request on {url}"}
        return delete_handler

    def create_post_handler(url, request_model=None):
        if request_model:
            async def post_handler(payload: request_model):
                return {"message": f"POST request on {url} with payload: {payload}"}
        else:
            async def post_handler():
                return {"message": f"POST request on {url}"}
        return post_handler

    def create_put_handler(url, request_model=None):
        if request_model:
            async def put_handler(payload: request_model):
                return {"message": f"PUT request on {url} with payload: {payload}"}
        else:
            async def put_handler():
                return {"message": f"PUT request on {url}"}
        return put_handler

    for route in config["routes"]:
        tag = route["tag"]
        url = route["url"]
        methods = route["methods"]
        response_fields = route["response"]
        request_body_fields = route["request_body"]
        print(tag)

        dynamic_model = create_dynamic_model("DynamicModel", response_fields)

        request_model = None
        if request_body_fields:
            create_dynamic_model("RequestModel", request_body_fields)

        for method in methods:
            if method == "GET":
                router.get(url, tags=[tag], response_model=dynamic_model)(create_get_handler(url))
            elif method == "DELETE":
                router.delete(url, tags=[tag])(create_delete_handler(url))
            elif method == "POST":
                router.post(url, tags=[tag], response_model=dynamic_model)(create_post_handler(url, request_model))
            elif method == "PUT":
                router.put(url, tags=[tag], response_model=dynamic_model)(create_put_handler(url, request_model))

    return router

dynamic_router = create_router_from_config(config)

app.include_router(dynamic_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8889, reload=True)
