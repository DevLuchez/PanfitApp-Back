from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models.dto.receipe import ReceipeDTO

receipe_routes = APIRouter()

@receipe_routes.post("/receipe")
def create_product(receipe: ReceipeDTO):
    from src.services.receipe_service import receipe_service
    receipe_ = receipe_service.create_receipe(receipe)
    return JSONResponse(content={"data":receipe_}, status_code=201)

@receipe_routes.get("/receipe")
def get_all_receipes():
    from src.services.receipe_service import receipe_service
    receipes = receipe_service.get_all_receipes()
    return JSONResponse(content={"data":receipes}, status_code=200)

@receipe_routes.get("/receipe/{receipe_id}")
def get_receipe_by_id(receipe_id: str):
    from src.services.receipe_service import receipe_service
    receipe = receipe_service.get_receipe_id(receipe_id)
    return JSONResponse(content={"data":receipe}, status_code=200)