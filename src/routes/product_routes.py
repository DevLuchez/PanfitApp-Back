from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import JSONResponse

from src.models.dto.product_dto import ProductDTO, ProductionRequestDTO, ProductionRequestARGS

from typing import Annotated

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

@product_routes.post("/production")
def create_product_request(product: ProductionRequestDTO):
    from src.services.product_service import product_service
    product_ = product_service.create_product_request(product)
    return JSONResponse(content={"data":product_}, status_code=201)

@product_routes.put("/production/{product_request_id}")
def update_product_request(product_request_id, production_args: ProductionRequestARGS):
    from src.services.product_service import product_service
    if not product_service.update_product_request(product_request_id, production_args):
        return JSONResponse(content={"error":"An error ocurred while updating production request"}, status_code=500)
    return JSONResponse(content={"data":"ok"}, status_code=200)

@product_routes.post("/production/{product_request_id}/finalize")
def finalize_production(product_request_id):
    from src.services.product_service import product_service
    response = product_service.finalize_product_request(product_request_id)
    return JSONResponse(content={"data":response}, status_code=200)

@product_routes.get("/production")
def get_all_production_request(production_args: Annotated[ProductionRequestARGS, Query()]):
    from src.services.product_service import product_service
    productions = product_service.get_production_request(production_args)
    return JSONResponse(content={'data':productions}, status_code=200)