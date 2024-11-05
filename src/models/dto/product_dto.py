from pydantic import BaseModel, Field

from typing import Optional, Literal

from datetime import datetime

class ProductDTO(BaseModel):
    name: str = Field(max_length=140)
    wheight: float = Field(gt=0)
    category: str = Field(max_length=140)
    receipe:str = Field(max_length=24)

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
    quantity: int = Field(gt=0)
    request_date: Optional[datetime] = None
    is_completed: Optional[bool] = False

    def to_mongoengine(self):
        from src.models.domain.product import ProductionRequest
        data = self.model_dump()
        data["request_date"] = data["request_date"] or datetime.now()
        return ProductionRequest(**data)