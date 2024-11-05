from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models.dto.product_dto import ProductDTO

product_routes = APIRouter()

@product_routes.post("/product")
def create_product(product: ProductDTO):
    from src.services.product_service import product_service
    product_ = product_service.create_product(product)
    return JSONResponse(content={"data":product_}, status_code=201)

@product_routes.get("/product")
def get_all_products():
    from src.services.product_service import product_service
    products = product_service.get_all_products()
    return JSONResponse(content={"data":products}, status_code=200)

@product_routes.get("/product/{product_id}")
def get_product_by_id(product_id: str):
    from src.services.product_service import product_service
    product = product_service.get_product_by_id(product_id)
    return JSONResponse(content={"data":product}, status_code=200) 

@product_routes.post("/product_request")
def create_product_request(product: ProductDTO):
    from src.services.product_service import product_service
    product_ = product_service.create_product(product)
    return JSONResponse(content={"data":product_}, status_code=201)