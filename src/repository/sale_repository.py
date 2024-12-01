from mongoengine import DoesNotExist
from src.models.domain.sale import Sale

from aggregation.pipelines import create_match_pipeline

class SaleRepository:
    def get_all(self):
        return Sale.objects.all()
    
    def get_by_id(self, sale_id):
        try:
            return Sale.objects.get(id=sale_id)
        except DoesNotExist:
            return None
    
    def get(self, **kwargs):
        try:
            return Sale.objects.get(**kwargs)
        except DoesNotExist:
            return None
    
    def get_by_args(self, **kwargs):
        return Sale.objects.filter(**kwargs)

    def create(self, sale: Sale):
        """Cria uma nova venda no banco de dados."""
        sale.save()
        return sale
    
    def find(self, limit, **kwargs):
        """Recupera um documento por qualquer campo,
        ou conjunto de campos.
        """
        return Sale.objects.aggregate(
            create_match_pipeline(limit=limit, **kwargs)
        )

    def update(self, sale_id: str, **kwargs):
        """Atualiza uma venda existente pelo ID."""
        sale = Sale.objects.get(id=sale_id)
        if sale:
            for key, value in kwargs.items():
                setattr(sale, key, value)
            sale.save()
            return sale
        return None