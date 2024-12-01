from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from src.models.dto.sale import SaleDTO, SaleArgs
from src.services.sale_services import sale_service

from typing import Annotated

sale_routes = APIRouter()

@sale_routes.post("/sale")
def create_sale(sale: SaleDTO):
    """
    Cria uma nova venda com base nos produtos e quantidades fornecidos.
    """
    sale_record = sale_service.process_sale(sale)
    if not sale_record:
        return JSONResponse(content={"error":'Unexpected Error'}, status_code=500)
    return JSONResponse(content={"data": sale_record}, status_code=201)

@sale_routes.get("/sale")
def create_sale(sale_args: Annotated[SaleArgs, Query()]):
    """
    Retorna todas as vendas
    """
    sale_record = sale_service.get_sale(sale_args)
    if not sale_record:
        return JSONResponse(content={"error":'Unexpected Error'}, status_code=500)
    return JSONResponse(content={"data": sale_record}, status_code=201)
    