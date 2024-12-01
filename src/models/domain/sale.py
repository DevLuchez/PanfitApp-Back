from mongoengine import (
    Document, StringField, 
    DecimalField, FloatField, 
    ReferenceField, DateTimeField, 
    ListField, DictField,
    ObjectIdField
)
from datetime import datetime
from decimal import Decimal
from bson import ObjectId

class Sale(Document):
    id = ObjectIdField(required=True, primary_key=True, default=lambda: ObjectId())
    sale_date = DateTimeField(default=datetime.now)
    products = ListField(DictField(), required=True)
    payment_type = StringField(choices=["credito", "debito", "dinheiro", "pix"])
    amount = DecimalField(min_value=0, precision=2, required=True)

    meta = {
        "collection": "panfit_sales",
    }

    def to_dict(self):
        sale_dict = {
            "id": str(self.id),
            "date": self.sale_date.isoformat(),
            "amount": float(self.amount),
            "payment_type": self.payment_type,
            "items": [
                {
                    "id": str(product["product"]),
                    "quantity": product["quantity"],
                    "sale_price": float(product.get("sale_price"))
                }
                for product in self.products
            ]
        }

        return sale_dict