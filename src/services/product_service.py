from fastapi import HTTPException

from src.models.dto.product_dto import ProductDTO

class ProductService:
    def __init__(self, product_repository, receipe_repository):
        self.product_repository = product_repository
        self.receipe_repository = receipe_repository

    def create_product(self, product: ProductDTO):
        receipe_id = product.receipe.id
        receipe = self.receipe_repository.get(receipe_id)

        if not receipe:
            raise HTTPException(status_code=404, detail=f"Receita com ID: {receipe_id} nao encontrada")

        product_db = self.item_repository.create(product.to_mongoengine())

        if not product_db:
            raise HTTPException(status_code=500, detail=f'Erro interno do servidor')
        
        return product_db.to_dict()

def create_product_service():
    from src.repository.product_repository import ProductRepository
    from src.repository.receipe_repository import ReceipeRepository
    return ProductService(ProductRepository(), ReceipeRepository())

product_service = create_product_service()         
