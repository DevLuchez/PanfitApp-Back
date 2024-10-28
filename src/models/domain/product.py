from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    ObjectIdField,
    FloatField
)

from bson import ObjectId

class Product(Document):
    id = ObjectIdField(required=True, primary_key=True, default=lambda: ObjectId())
    name = StringField(required=True, max_length=140)
    wheight = FloatField(min_value=0)
    category = StringField(required=True)
    receipe = ReferenceField("Receipe", required=True)

    meta = {"collection":"panfit_products"}

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