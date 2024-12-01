from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    ObjectIdField,
    FloatField,
    IntField,
    DateTimeField, 
    DecimalField,
    BooleanField
)

from bson import ObjectId
from datetime import datetime

class Product(Document):
    id = ObjectIdField(required=True, primary_key=True, default=lambda: ObjectId())
    name = StringField(required=True, max_length=140)
    wheight = FloatField(required=True, min_value=0)
    stock_wheight = FloatField(required=True, min_value=0, default=0)
    category = StringField(required=True)
    receipe = ReferenceField("Receipe", required=True)
    sale_price = DecimalField(min_value=0, precision=2, required=True)


    meta = {
        "collection": "panfit_products",
        "indexes": [
            {
                "fields": ["name"],
                "unique": True, 
            }
        ]
    }

    def to_dict(self, verbose=False):
        product_dict = {
            "id":str(self.id),
            "name":self.name,
            "wheight":self.wheight,
            "category":self.category,
            "receipe":{
                "id":str(self.receipe.id)
            }
        }

        if verbose:
            product_dict['receipe'].update({
                "items":[item.to_dict() for item in self.receipe.items]
            })
        
        return product_dict

class ProductMovement(Document):
    MOVEMENT_TYPES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('venda', 'Venda'),
        ('vencido', 'Vencido'),
        ('ajuste', 'Ajuste')
    )
    
    product = ReferenceField(Product, required=True)
    movement_type = StringField(choices=MOVEMENT_TYPES, required=True)
    quantity = IntField(required=True, min_value=1)
    movement_date = DateTimeField(default=datetime.now())
    observation = StringField(max_length=200)
    sale_price = DecimalField(min_value=0, precision=2)
    
    meta = {
        'collection': 'panfit_product_movements',
        'indexes': [
            'movement_date',
            'product'
        ],
        'ordering': ['-movement_date']
    }

    def to_dict(self):
        return {
            "product": {
                "id": str(self.product.id),
                "name": self.product.name,
                "wheight": self.product.wheight,
                "category": self.product.category,
                "receipe": str(self.product.receipe.id)
            },
            "movement_type": self.movement_type,
            "quantity": self.quantity,
            "movement_date": self.movement_date.isoformat(),
            "observation": self.observation,
            "sale_price": float(self.sale_price) if self.sale_price else None
        }
    
class ProductRequest(Document):
    id = ObjectIdField(required=True, primary_key=True, default=lambda: ObjectId())
    product = ReferenceField("Product", required=True)
    quantity = IntField(required=True, min_value=1)
    request_date = DateTimeField(default=datetime.now())
    status = StringField(
        choices=["produzido", "não produzido", "em_produção"],
        default="não produzido"
    )
    
    meta = {
        "collection": "panfit_production_requests",
        "indexes": [
            "request_date",
            "product",
            "status"
        ]
    }

    def to_dict(self):
        return {
            "id": str(self.id),
            "product": {
                "id": str(self.product.id),
                "name": self.product.name
            },
            "quantity": self.quantity,
            "request_date": self.request_date.isoformat(),
            "status": self.status
        }

    def set_status(self, new_status):
        if new_status not in ["produzido", "não produzido", "em_produção"]:
            raise ValueError("Invalid status")
        self.status = new_status
        self.save()