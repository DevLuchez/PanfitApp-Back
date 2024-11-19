from mongoengine import DoesNotExist
from src.models.domain.receipe import Receipe, ItemWheight
from src.models.domain.item import Item

from aggregation.pipelines import create_match_pipeline

class ReceipeRepository:
    def create(self, receipe: Receipe) -> Receipe:
        """Cria uma nova receita no banco de dados."""
        receipe.save()
        return receipe

    def get(self, receipe_id: str):
        """Recupera uma receita pelo ID."""
        try:
            return Receipe.objects.get(id=receipe_id)
        except DoesNotExist:
            return None
        
    def find(self, limit, **kwargs):
        """Recupera um documento por qualquer campo,
        ou conjunto de campos.
        """
        return Receipe.objects.aggregate(create_match_pipeline(limit=limit, **kwargs))
    
    def get_by_product_id(self, product_id: str):
        try:
            return Receipe.objects.get(product_id=product_id)
        except DoesNotExist:
            return None
    
    def get_all(self):
        return Receipe.objects.all()

    def update(self, receipe_id: str, **kwargs):
        """Atualiza uma receita existente pelo ID."""
        receipe = self.get(receipe_id)
        if receipe:
            if 'category' in kwargs:
                receipe.category = kwargs['category']
            if 'items' in kwargs:
                item_wheight_objects = [ItemWheight(item=item['item'], wheight=item['wheight']) for item in kwargs['items']]
                receipe.items = item_wheight_objects
            receipe.save()
            return receipe
        return None

    def delete(self, receipe_id: str):
        """Remove uma receita pelo ID."""
        receipe = self.get(receipe_id)
        if receipe:
            receipe.delete()
            return True
        return False

    def list_all(self):
        """Lista todas as receitas."""
        return Receipe.objects.all()
