from fastapi import HTTPException

from src.models.dto.receipe import ReceipeDTO
from src.models.domain.receipe import ItemWheight

class ReceipeService:
    def __init__(self, receipe_repository, product_repository):
        self.receipe_repository = receipe_repository
        self.product_repository = product_repository

    def create_receipe(self, receipe: ReceipeDTO):
        
        print(str(receipe))

        item_wheight = []
        not_found = []

        for item in receipe.items:
            item_id = item.id
            item_db = self.product_repository.get(item_id)

            if not item_db:
                not_found.append(item_id)

        if not_found:
            raise HTTPException(
                status_code=404, detail={"itens":not_found, "message":"Itens nao encontrados"}
            )
            
        item_wheight.append(ItemWheight(item=item_db, wheight=item.wheight))

        new_receipe = receipe.to_mongoengine()
        new_receipe.items = item_wheight

        receipe_db = self.receipe_repository.create(new_receipe)

        if not receipe_db:
            raise HTTPException(status_code=500, detail='Erro interno do servidor')
        
        return receipe_db.to_dict()

def create_receipe_service():
    from src.repository.receipe_repository import ReceipeRepository
    from src.repository.product_repository import ProductRepository
    return ReceipeService(ReceipeRepository(), ProductRepository())

receipe_service = create_receipe_service()