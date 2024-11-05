from pydantic import BaseModel, Field, field_validator
from typing import Optional
from src.utils.gtin import validate_gtin

class ItemDTO(BaseModel):
    name: str = Field(max_length=140)
    GTIN: str = Field(min_length=14, max_length=14)
    wheight: float = Field(gt=0)
    category: str = Field(max_length=140)

    #@field_validator('GTIN')
    #def validate_gtin_field(cls, gtin: str) -> str:
    #    if not validate_gtin(gtin):
    #        raise ValueError(f"GTIN: {gtin} inválido.")
    #    return gtin
    
    def to_mongoengine(self):
        from src.models.domain.item import Item
        return Item(**self.model_dump())

class ItemArgs(BaseModel):
    name: Optional[str] = Field(max_length=140)
    GTIN: str = Field(min_length=14, max_length=14)
    wheight: float = Field(gt=0)
    category: str = Field(max_length=140)

    #@field_validator('GTIN')
    #def validate_gtin_field(cls, gtin: str) -> str:
    #    if not validate_gtin(gtin):
    #        raise ValueError(f"GTIN: {gtin} inválido.")
    #    return gtin
    
    def to_mongoengine(self):
        from src.models.domain.item import Item
        return Item(**self.model_dump())
