from mongoengine import DoesNotExist
from src.models.domain.product import ProductRequest

from aggregation.pipelines import create_match_pipeline

class ProductRequestRepository:
    def get_all(self):
        return ProductRequest.objects.all()
    
    def get_by_id(self, production_id):
        try:
            return ProductRequest.objects.get(id=production_id)
        except DoesNotExist:
            return None
    
    def get(self, **kwargs):
        try:
            return ProductRequest.objects.get(**kwargs)
        except DoesNotExist:
            return None

    def create(self, product: ProductRequest):
        """Cria um novo produto no banco de dados."""
        product.save()
        return product
    
    def find(self, limit, **kwargs):
        """Recupera um documento por qualquer campo,
        ou conjunto de campos.
        """
        return ProductRequest.objects.aggregate(
            create_match_pipeline(limit=limit, **kwargs)
        )

    def update(self, request_id: str, **kwargs):
        """Atualiza um produto existente pelo ID."""
        product = ProductRequest.objects.get(id=request_id)
        if product:
            for key, value in kwargs.items():
                setattr(product, key, value)
            product.save()
            return product
        return None