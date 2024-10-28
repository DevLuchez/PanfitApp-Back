from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    ObjectIdField,
    FloatField,
    EmbeddedDocument,
    EmbeddedDocumentListField
)

from bson import ObjectId

class ItemWheight(EmbeddedDocument):
    item = ReferenceField("Item", required=True)
    wheight = FloatField(Required=True, min_value=0)

    def to_dict(self, verbose=False):
        item_dict =  {
            "id":str(self.item.id),
            "name":self.item.name,
            "wheight":self.wheight,
        }

        if verbose:
            item_dict['item'].update({
                "GTIN":self.GTIN,
                "wheight":self.wheight,
                "category":self.category
            })
        
        return item_dict

class Receipe(Document):
    id = ObjectIdField(required=True, primary_key=True, default=lambda: ObjectId())
    category = StringField(max_length=140, required=True)
    items = EmbeddedDocumentListField(ItemWheight, required=True)

    meta = {"collection":"panfit_receipes"}

    def to_dict(self, verbose=False):
        return {
            "id":str(self.id),
            "category":self.category,
            "items":[item.to_dict(verbose=verbose) for item in self.items],
            "wheight":sum([item.wheight for item in self.items])
        }