from mongoengine import DoesNotExist
from src.models.domain.product import Product

from aggregation.pipelines import create_match_pipeline

class ProductRepository:
    def create(self, product: Product):
        """Cria um novo produto no banco de dados."""
        product.save()
        return product

    def get(self, product_id: str):
        """Recupera um produto pelo ID."""
        try:
            return Product.objects.get(id=product_id)
        except DoesNotExist:
            return None
    
    def get_all(self):
        """Recupera todos os produtos"""
        return Product.objects.all()
    
    def find(self, limit, **kwargs):
        """Recupera um documento por qualquer campo,
        ou conjunto de campos.
        """
        return Product.objects.aggregate(create_match_pipeline(limit=limit, **kwargs))
    
    def find_by_pipeline(self, pipeline: list[dict]):
        "Recupera documentos com pipeline dinamico"
        return Product.objects(id__in=pipeline)

    def update(self, product_id: str, **kwargs):
        """Atualiza um produto existente pelo ID."""
        product = self.get(product_id)
        if product:
            for key, value in kwargs.items():
                setattr(product, key, value)
            product.save()
            return product
        return None

    def delete(self, product_id: str):
        """Remove um produto pelo ID."""
        product = self.get(product_id)
        if product:
            product.delete()
            return True
        return False

    def list_all(self):
        """Lista todos os produtos."""
        return Product.objects.all()
