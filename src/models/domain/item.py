from mongoengine import (
    Document,
    StringField,
    ObjectIdField,
    FloatField
)

from bson import ObjectId

class Item(Document):
    id = ObjectIdField(required=True, primary_key=True, default=lambda: ObjectId())
    name = StringField(required=True, max_length=140)
    GTIN = StringField(required=False, max_length=14)
    wheight = FloatField(min_value=0)
    category = StringField(required=True)

    meta = {"collection":"panfit_items"}

    def to_dict(self):
        return {
            "id":str(self.id),
            "name":self.name,
            "GTIN":self.GTIN,
            "wheight":self.wheight,
            "category":self.category
        }
    