from mongoengine import (
    Document,
    StringField,
    ObjectIdField,
    FloatField,
    ReferenceField,
    IntField,
    DateTimeField,
    DecimalField
)

from bson import ObjectId
from datetime import datetime

class Item(Document):
    id = ObjectIdField(required=True, primary_key=True, default=lambda: ObjectId())
    name = StringField(required=True, max_length=140)
    GTIN = StringField(required=False, max_length=14)
    wheight = FloatField(min_value=0)
    category = StringField(required=True)
    stock_wheight = FloatField(min_value=0)

    meta = {"collection":"panfit_items"}

    def to_dict(self):
        return {
            "id":str(self.id),
            "name":self.name,
            "GTIN":self.GTIN,
            "wheight":self.wheight,
            "category":self.category
        }

class ItemMovement(Document):
    MOVEMENT_TYPES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('ajuste', 'Ajuste'),
        ('perda', 'Perda')
    )
    
    item = ReferenceField(Item, required=True)
    movement_type = StringField(choices=MOVEMENT_TYPES, required=True)
    quantity = IntField(required=True, min_value=1)
    movement_date = DateTimeField(default=datetime.now())
    observation = StringField(max_length=200)
    cost_price = DecimalField(min_value=0, precision=2)
    
    meta = {
        'collection': 'panfit_item_movements',
        'indexes': [
            'movement_date',
            'item'
        ],
        'ordering': ['-movement_date']
    }

    def to_dict(self):
        return {
            "item": {
                "id": str(self.item.id),
                "name": self.item.name,
                "category": self.item.category,
                "stock_weight": self.item.stock_weight
            },
            "movement_type": self.movement_type,
            "quantity": self.quantity,
            "movement_date": self.movement_date.isoformat(),
            "observation": self.observation,
            "cost_price": float(self.cost_price) if self.cost_price else None
        }