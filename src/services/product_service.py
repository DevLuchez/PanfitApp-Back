from fastapi import HTTPException

from src.models.dto.product_dto import ProductDTO

class ProductService:
    def __init__(self, product_repository, receipe_repository):
        self.product_repository = product_repository
        self.receipe_repository = receipe_repository

    def create_product(self, product: ProductDTO):
        receipe_id = product.receipe
        receipe = self.receipe_repository.get(receipe_id)

        if not receipe:
            raise HTTPException(status_code=404, detail=f"Receita com ID: {receipe_id} nao encontrada")
        

        product_db = self.product_repository.create(product.to_mongoengine())

        if not product_db:
            raise HTTPException(status_code=500, detail=f'Erro interno do servidor')
        
        return product_db.to_dict()
    
    def get_all_products(self):
        products_db = self.product_repository.get_all()
        if not products_db:
            raise HTTPException(status_code=404, detail=f'No products found')
        
        products = [product.to_dict() for product in products_db]
        return products
    
    def get_product_by_id(self, product_id: str):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f'Product with ID: {product_id} not found')
        
        return product.to_dict()

def create_product_service():
    from src.repository.product_repository import ProductRepository
    from src.repository.receipe_repository import ReceipeRepository
    return ProductService(ProductRepository(), ReceipeRepository())

product_service = create_product_service()         
