from pydantic import BaseModel, Field

from typing import Literal, Optional

class ProductQuantity(BaseModel):
    id: str
    quantity: int

class SaleDTO(BaseModel):
    products: list[ProductQuantity]
    payment_type: Literal["credito", "debito", "dinheiro", "pix"]

class SaleArgs(BaseModel):
    products: Optional[list[ProductQuantity]] = None
    payment_type: Optional[Literal["credito", "debito", "dinheiro", "pix"]] = None