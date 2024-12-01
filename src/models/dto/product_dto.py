from pydantic import BaseModel, Field

from typing import Optional, Literal, Union
from types import NoneType

from datetime import datetime

class ProductDTO(BaseModel):
    name: str = Field(max_length=140)
    wheight: float = Field(gt=0)
    category: str = Field(max_length=140)
    receipe: str = Field(max_length=24)
    sale_price: float = Field(ge=0)

    def to_mongoengine(self):
        from src.models.domain.product import Product
        return Product(**self.model_dump())

class ProductMovementDTO(BaseModel):
    product: str = Field(max_length=24)
    movement_type: Literal["entrada", "saida", "venda", "vencido", "ajuste"]
    quantity: int = Field(gt=0)
    movement_date: Optional[datetime] = None
    observation: Optional[str] = Field(max_length=200)
    sale_price: Optional[float] = Field(ge=0)

    def to_mongoengine(self):
        from src.models.domain.product import ProductMovement
        data = self.model_dump()
        data["movement_date"] = data["movement_date"] or datetime.now()
        return ProductMovement(**data)

class ProductionRequestDTO(BaseModel):
    product: str = Field(max_length=24)
    quantity: float = Field(gt=0)
    request_date: Optional[datetime] = None
    status: Optional[Literal["produzido", "não produzido", "em_produção"]] = None

    def to_mongoengine(self):
        from src.models.domain.product import ProductRequest
        data = self.model_dump()
        data["request_date"] = data["request_date"] or datetime.now()
        return ProductRequest(**data)

class ProductionRequestARGS(BaseModel):
    #product: str = Field(max_length=24)
    quantity: Optional[Union[int, NoneType]] = Field(gt=0, default=None)
    request_date: Optional[datetime] = None
    status: Optional[Literal["produzido", "não produzido", "em_produção"]] = None