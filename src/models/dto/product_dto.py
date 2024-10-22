from pydantic import BaseModel, Field

from typing import Optional

from src.utils.gtin import validate_gtin

class ProductDTO(BaseModel):
    name: str = Field(max_length=140)
    GTIN: Optional[str] = Field(max_length=14)
    wheight: float = Field(gt=0)
    category: str = Field(max_length=140)
    receipe:str = Field(max_length=13)

    def to_mongoengine(self):
        from src.models.domain.product import Product
        return Product(**self.model_dump())