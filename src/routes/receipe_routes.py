from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models.dto.receipe import ReceipeDTO

receipe_routes = APIRouter()

@receipe_routes.post("/receipe")
def create_product(receipe: ReceipeDTO):
    from src.services.receipe_service import receipe_service
    receipe_ = receipe_service.create_receipe(receipe)
    return JSONResponse(content={"data":receipe_}, status_code=201)