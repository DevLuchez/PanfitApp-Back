from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models.dto.item import ItemDTO

item_routes = APIRouter()

@item_routes.post("/item")
def create_product(item: ItemDTO):
    from src.services.item_service import item_service
    item_ = item_service.create_item(item)
    return JSONResponse(content={"data":item_}, status_code=201)

@item_routes.get("/item")
def get_all_items():
    from src.services.item_service import item_service
    items = item_service.get_all_items()
    return JSONResponse(content={"data":items}, status_code=200)

@item_routes.get("/item/{item_id}")
def get_all_items(item_id: str):
    from src.services.item_service import item_service
    item = item_service.get_item_by_id(item_id)
    return JSONResponse(content={"data":item}, status_code=200)