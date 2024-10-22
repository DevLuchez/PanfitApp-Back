from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models.dto.product_dto import ProductDTO

product_routes = APIRouter()

@product_routes.post("/product")
def create_product(product: ProductDTO):
    from src.services.product_service import product_service
    product_ = product_service.create_product(product)
    return JSONResponse(content={"data":product_}, status_code=201)