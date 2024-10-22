from mongoengine import DoesNotExist
from src.models.domain.item import Item

class ItemRepository:
    def create(self, item: Item):
        """Cria um novo item no banco de dados."""
        item.save()
        return item

    def get(self, item_id: str):
        """Recupera um item pelo ID."""
        try:
            return Item.objects.get(id=item_id)
        except DoesNotExist:
            return None

    def update(self, item_id: str, **kwargs):
        """Atualiza um item existente pelo ID."""
        item = self.get(item_id)
        if item:
            for key, value in kwargs.items():
                setattr(item, key, value)
            item.save()
            return item
        return None

    def delete(self, item_id: str):
        """Remove um item pelo ID."""
        item = self.get(item_id)
        if item:
            item.delete()
            return True
        return False

    def list_all(self):
        """Lista todos os itens."""
        return Item.objects.all()
