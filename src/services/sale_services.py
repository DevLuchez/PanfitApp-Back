from fastapi import HTTPException
from bson import ObjectId

from src.models.domain.item import ItemMovement
from src.models.domain.product import ProductMovement

from src.models.domain.sale import Sale
from src.models.dto.sale import SaleDTO, SaleArgs

from mongoengine import get_db
from datetime import datetime

from bson import ObjectId

class SaleService:
    def __init__(self, product_repository, item_repository, sale_repository, receipe_repository):
        self.product_repository = product_repository
        self.item_repository = item_repository
        self.sale_repository = sale_repository
        self.receipe_repository = receipe_repository

    def process_sale(self, sale: SaleDTO):
        db = get_db()
        with db.client.start_session() as session:
            try:
                with session.start_transaction():
                    product_ids = [ObjectId(product.id) for product in sale.products]
                    products = list(self.product_repository.find_by_pipeline(product_ids))
                    sale_id = ObjectId()

                    if len(products) != len(sale.products):
                        not_found = [
                            item.id for item in sale.products
                            if str(item.id) not in [str(product.id) for product in products]
                        ]
                        raise HTTPException(
                            status_code=404,
                            detail={
                                "products": not_found,
                                "message": "Products not found",
                            }
                        )

                    total_amount = 0 

                    for sale_item in sale.products:
                        product = next((p for p in products if str(p.id) == sale_item.id), None)
                        if not product:
                            continue
                        
                        if product.stock_wheight < (product.wheight * sale_item.quantity):
                            raise HTTPException(
                                status_code=409,
                                detail=(
                                    f"Insufficient stock for product ID: {sale_item.id}. "
                                    f"Required: {product.wheight * sale_item.quantity}, Available: {product.stock_wheight}"
                                )
                            )

                        # Calcula o preço da venda para o item
                        sale_price = product.sale_price
                        item_total = sale_price * sale_item.quantity
                        total_amount += item_total

                        # Busca a receita do produto
                        recipe = self.receipe_repository.get(product.receipe.id)
                        if not recipe:
                            raise HTTPException(
                                status_code=404,
                                detail=f"Recipe for product ID: {product.id} not found"
                            )

                        # Processa cada ingrediente da receita
                        for recipe_item in recipe.items:
                            ingredient = self.item_repository.get_by_id(recipe_item.item.id)
                            if not ingredient:
                                raise HTTPException(
                                    status_code=404,
                                    detail=f"Ingredient with ID: {recipe_item.item.id} not found"
                                )

                            required_quantity = recipe_item.wheight * sale_item.quantity
                            if ingredient.stock_wheight < required_quantity:
                                raise HTTPException(
                                    status_code=409,
                                    detail=(
                                        f"Insufficient stock for ingredient ID: {recipe_item.item.id}. "
                                        f"Required: {required_quantity}, Available: {ingredient.stock_wheight}"
                                    )
                                )

                            # Atualiza o estoque do ingrediente
                            new_stock_wheight = ingredient.stock_wheight - required_quantity
                            self.item_repository.update(
                                ingredient.id,
                                stock_wheight=new_stock_wheight,
                            )

                            # Registra o movimento do ingrediente
                            item_movement = ItemMovement(
                                item=ingredient,
                                movement_type="saida",
                                quantity=required_quantity,
                                movement_date=datetime.now(),
                                observation=f"Used in sale of product {product.name} (ID: {product.id})"
                            )
                            item_movement.save()

                        # Atualiza o estoque do produto vendido
                        new_product_stock_wheight = product.stock_wheight - (product.wheight * sale_item.quantity)
                        self.product_repository.update(
                            product.id,
                            stock_wheight=new_product_stock_wheight,
                        )

                        # Registra o movimento do produto vendido
                        product_movement = ProductMovement(
                            product=product,
                            movement_type="venda",
                            quantity=sale_item.quantity,
                            movement_date=datetime.now(),
                            observation=f"Sold in sale (Sale ID: {str(sale_id)})"
                        )
                        product_movement.save()

                    # Registra a venda como finalizada
                    sale_record = Sale(
                        id=sale_id,
                        sale_date=datetime.now(),
                        products=[{
                            "product": str(sale_item.id),
                            "quantity": sale_item.quantity,
                            "sale_price": float(next((p.sale_price for p in products if str(p.id) == sale_item.id), 0)),
                        } for sale_item in sale.products],
                        amount=total_amount,
                        payment_type=sale.payment_type,
                    )
                    self.sale_repository.create(sale_record)

  
                    return {
                        "message": "Sale processed successfully",
                        "sale_id": str(sale_record.id),
                    }
            except HTTPException as e:
                raise e

    def get_sale(self, sale_args: SaleArgs):
        if sale_args is not None:
            request_args = sale_args.model_dump(exclude_unset=True)
        else:
            request_args = None
        
        if request_args:
            sale_db = self.sale_repository.get_by_args(**request_args)
        else:
            sale_db = self.sale_repository.get_all()

        if not sale_db:
            raise HTTPException(status_code=404, detail=f'Sales not found')
        
        if len(sale_db) > 0:
            sales = [sale.to_dict() for sale in sale_db]
        else:
            sales = sale_db.to_dict()

        return sales


def create_sale_service():
    from src.repository.product_repository import ProductRepository
    from src.repository.receipe_repository import ReceipeRepository
    from src.repository.sale_repository import SaleRepository
    from src.repository.item_repository import ItemRepository
    return SaleService(ProductRepository(), ItemRepository(), SaleRepository(), ReceipeRepository())

sale_service = create_sale_service()        