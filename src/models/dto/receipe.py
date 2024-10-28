from pydantic import BaseModel, Field

from typing import Optional

class Item(BaseModel):
    id: str
    wheight: float = Field(gt=0)

class ReceipeDTO(BaseModel):
    category: str = Field(max_length=140)
    items: list[Item]
    verbose: Optional[bool] = Field(default=False)

    def to_mongoengine(self):
        from src.models.domain.receipe import Receipe
        return Receipe(category=self.category)