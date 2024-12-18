from mongoengine import DoesNotExist
from src.models.domain.item import Item

from aggregation.pipelines import create_match_pipeline

class ItemRepository:
    def create(self, item: Item):
        """Cria um novo item no banco de dados."""
        item.save()
        return item

    def get_by_id(self, item_id: str):
        """Recupera um item pelo ID."""
        try:
            return Item.objects.get(id=item_id)
        except DoesNotExist:
            return None
    
    def get(self, **kwargs):
        try:
            return Item.objects.get(**kwargs)
        except DoesNotExist:
            return None
        
    def get_all(self):
        """Recupera todos os itens do banco"""
        return Item.objects.all()
        
    def find(self, limit, **kwargs):
        """Recupera um documento por qualquer campo,
        ou conjunto de campos.
        """
        return Item.objects.aggregate(create_match_pipeline(limit=limit, **kwargs))
    
    def find_by_pipeline(self, pipeline: list[dict]):
        "Recupera documentos com pipeline dinamico"
        return Item.objects(id__in=pipeline)

    def update(self, item_id: str, **kwargs):
        """Atualiza um item existente pelo ID."""
        item = Item.objects.get(id=item_id)
        if item:
            for key, value in kwargs.items():
                setattr(item, key, value)
            item.save() 
            return item
        return None

    def delete(self, item_id: str):
        """Remove um item pelo ID."""
        item = Item.objects.get(id=item_id)
        if item:
            item.delete()
            return True
        return False

    def list_all(self):
        """Lista todos os itens."""
        return Item.objects.all()
