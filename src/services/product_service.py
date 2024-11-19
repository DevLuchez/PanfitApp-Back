from fastapi import HTTPException

from src.models.dto.product_dto import (
        ProductDTO, ProductionRequestDTO, ProductionRequestARGS
)

class ProductService:
    def __init__(self, product_repository, receipe_repository, request_repository):
        self.product_repository = product_repository
        self.receipe_repository = receipe_repository
        self.request_repository = request_repository
        self.item_repository = item_repository

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
    
    def create_product_request(self, product_request: ProductionRequestDTO):
        product_id = product_request.product
        product = self.product_repository.get(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail=f'Product with ID: {product_id} not found')
        
        request_db = self.request_repository.create(product_request.to_mongoengine())

        if not request_db:
            raise HTTPException(status_code=500, detail='Erro interno do servidor ao salvar a solicitacao de produto')
        
        return request_db.to_dict()
    

    #TODO: TERMINAR ISSO DAQUI
    def update_product_request(self, product_request_id, product_request: ProductionRequestARGS):
        production = self.request_repository.update(product_request_id, **product_request.model_dump())

        production = self.request_repository.get(product_request_id)

        if not production:
            raise HTTPException(status_code=404, detail=f'Production Request with ID: {product_request_id} not found')
        
        receipe = self.receipe_repository.get_by_product_id(production.product)

        if not receipe:
            raise HTTPException(status_code=404, detail=f"Receipe not found")
        
        for item in receipe.items:
            item_db = self.item_repository.get(item.id)

        return True
    
    def get_all_product_request(self):
        production_db = self.request_repository.get_all()
        if not production_db:
            raise HTTPException(status_code=404, detail=f'No production request found')
        
        production = [production.to_dict() for production in production_db]
        return production

def create_product_service():
    from src.repository.product_repository import ProductRepository
    from src.repository.receipe_repository import ReceipeRepository
    from src.repository.request_repository import ProductRequestRepository
    return ProductService(ProductRepository(), ReceipeRepository(), ProductRequestRepository())

product_service = create_product_service()         
