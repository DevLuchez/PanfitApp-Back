from fastapi import HTTPException

from src.models.dto.product_dto import (
        ProductDTO, ProductionRequestDTO, ProductionRequestARGS
)

from mongoengine import NotUniqueError, get_db
from datetime import datetime

from src.models.domain.item import ItemMovement
from src.models.domain.product import ProductMovement

class ProductService:
    def __init__(self, product_repository, receipe_repository, request_repository, item_repository):
        self.product_repository = product_repository
        self.receipe_repository = receipe_repository
        self.request_repository = request_repository
        self.item_repository = item_repository

    def create_product(self, product: ProductDTO):
        receipe_id = product.receipe
        receipe = self.receipe_repository.get(receipe_id)

        if not receipe:
            raise HTTPException(status_code=404, detail=f"Receita com ID: {receipe_id} nao encontrada")
        
        try:
            product_db = self.product_repository.create(product.to_mongoengine())
        except NotUniqueError:
            raise HTTPException(status_code=400, detail=f"Product: {product.name} already exists")

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
    
    def get_production_request(self, product_request_args: ProductionRequestARGS):

        if product_request_args is not None:
            request_args = product_request_args.model_dump(exclude_unset=True)
        else:
            request_args = None
        
        if request_args:
            production_db = self.request_repository.get_by_args(**request_args)
        else:
            production_db = self.request_repository.get_all()

        if not production_db:
            raise HTTPException(status_code=404, detail=f'Production Requests not found')
        
        if len(production_db) > 0:
            productions = [production.to_dict() for production in production_db]
        else:
            productions = production_db.to_dict()

        return productions

    def update_product_request(self, product_request_id, product_request_args: ProductionRequestARGS):

        production = self.request_repository.get_by_id(product_request_id)

        if not production:
            raise HTTPException(status_code=404, detail=f'Production Request with ID: {product_request_id} not found')
        
        if production.status == "produzido" and product_request_args.status != "produzido":
            raise HTTPException(status_code=409, detail=f'Production with status: produzido cannot be changed')
          
        production = self.request_repository.update(
            product_request_id, 
            **product_request_args.model_dump(exclude_unset=True)
        )

        if not production:
            return False

        return True


    #TODO: registrar produtos com novo campo stock_wheigth
    def finalize_product_request(self, request_id: str):
        db = get_db()  # Obtém a conexão com o banco
        with db.client.start_session() as session:
            try:
                with session.start_transaction(): 
                    production_request = self.request_repository.get(id=request_id)
                    if not production_request:
                        raise HTTPException(
                            status_code=404,
                            detail=f"Production request with ID: {request_id} not found"
                        )

                    if production_request.status == "produzido":
                        raise HTTPException(
                            status_code=409,
                            detail=f"Production request with ID: {request_id} is already completed"
                        )

                    # Busca o produto
                    product = self.product_repository.get(production_request.product.id)
                    if not product:
                        raise HTTPException(
                            status_code=404,
                            detail=f"Product with ID: {production_request.product} not found"
                        )

                    # Busca a receita do produto
                    recipe = self.receipe_repository.get(product.receipe.id)
                    if not recipe:
                        raise HTTPException(
                            status_code=404,
                            detail=f"Recipe for product ID: {product.id} not found"
                        )
                    
                    for recipe_item in recipe.items:
                        ingredient = self.item_repository.get_by_id(recipe_item.item.id)
                        if not ingredient:
                            raise HTTPException(
                                status_code=404,
                                detail=f"Ingredient with ID: {recipe_item.item.id} not found"
                            )

                        if ingredient.stock_wheight < (recipe_item.wheight * production_request.quantity):
                            raise HTTPException(
                                status_code=409,
                                detail=(
                                    f"Insufficient stock for ingredient ID: {recipe_item.id}. "
                                    f"Required: {recipe_item.wheight * production_request.quantity}, Available: {ingredient.stock_wheight}"
                                )
                            )

                        # Atualiza o estoque do ingrediente
                        new_stock_wheight = ingredient.stock_wheight - (recipe_item.wheight * production_request.quantity)
                        self.item_repository.update(
                            ingredient.id,
                            stock_wheight=new_stock_wheight,
                        )

                        # Registra o movimento do item
                        item_movement = ItemMovement(
                            item=ingredient,
                            movement_type='saida',
                            quantity=recipe_item.wheight,
                            movement_date=datetime.now(),
                            observation=f"Utilizado na produção do produto {product.name} (ID: {product.id})"
                        )
                        item_movement.save()

                # Atualiza o estoque do produto
                new_product_stock_wheight = product.stock_wheight + (product.wheight * production_request.quantity)
                self.product_repository.update(
                    product.id,
                    stock_wheight=new_product_stock_wheight,
                )

                # Registra o movimento do produto
                product_movement = ProductMovement(
                    product=product,
                    movement_type='entrada',
                    quantity=product.wheight,
                    movement_date=datetime.now(),
                    observation=f"Produção concluída (ID da requisição: {request_id})"
                )
                product_movement.save()

                # Atualiza o status da requisição de produção
                self.request_repository.update(
                    production_request.id,
                    status='produzido',
                )

                # Finaliza a transação
                return {
                    "message": "Production request finalized successfully",
                    "product_id": str(product.id),
                    "updated_product_stock": new_product_stock_wheight,
                }

            except Exception as e:
                raise HTTPException(status_code=e.status_code, detail=f"Error finalizing production request: {e.detail}")

def create_product_service():
    from src.repository.product_repository import ProductRepository
    from src.repository.receipe_repository import ReceipeRepository
    from src.repository.request_repository import ProductRequestRepository
    from src.repository.item_repository import ItemRepository
    return ProductService(ProductRepository(), ReceipeRepository(), ProductRequestRepository(), ItemRepository())

product_service = create_product_service()         
