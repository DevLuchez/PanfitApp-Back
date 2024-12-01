from pydantic import BaseModel, Field, field_validator
from typing import Optional
from src.utils.gtin import validate_gtin

class ItemDTO(BaseModel):
    name: str = Field(max_length=140)
    GTIN: str = Field(min_length=14, max_length=14)
    wheight: float = Field(gt=0)
    category: str = Field(max_length=140)
    quantity: int = Field(gt=0)

    #@field_validator('GTIN')
    #def validate_gtin_field(cls, gtin: str) -> str:
    #    if not validate_gtin(gtin):
    #        raise ValueError(f"GTIN: {gtin} inválido.")
    #    return gtin
    
    def to_mongoengine(self):
        from src.models.domain.item import Item
        item = self.model_dump()

        if item.get('quantity'):
            del item['quantity']

        return Item(**item)

class ItemArgs(BaseModel):
    name: Optional[str] = Field(max_length=140)
    GTIN: str = Field(min_length=14, max_length=14)
    wheight: float = Field(gt=0)
    category: str = Field(max_length=140)
    stock_wheight: float = Field(gt=0)

    #@field_validator('GTIN')
    #def validate_gtin_field(cls, gtin: str) -> str:
    #    if not validate_gtin(gtin):
    #        raise ValueError(f"GTIN: {gtin} inválido.")
    #    return gtin
    
    def to_mongoengine(self):
        from src.models.domain.item import Item
        return Item(**self.model_dump())
