from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models.dto.item import ItemDTO

item_routes = APIRouter()

@item_routes.post("/item")
def create_product(item: ItemDTO):
    from src.services.item_service import item_service
    item_ = item_service.create_item(item)
    return JSONResponse(content={"data":item_}, status_code=201)