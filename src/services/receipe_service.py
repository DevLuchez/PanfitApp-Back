from fastapi import HTTPException
from bson import ObjectId

from src.models.dto.receipe import ReceipeDTO
from src.models.domain.receipe import ItemWheight

class ReceipeService:
    def __init__(self, receipe_repository, item_repository):
        self.receipe_repository = receipe_repository
        self.item_repository = item_repository

    def create_receipe(self, receipe: ReceipeDTO):

        existing_items = list(self.item_repository.find_by_pipeline([ObjectId(item.id) for item in receipe.items]))

        if len(existing_items) != len(receipe.items):

            not_found = []
            for item in receipe.items:
                if str(item.id) not in [str(item.id) for item in existing_items]:
                    not_found.append(item.id)

            if not_found:
                raise HTTPException(
                status_code=404, detail={
                    "itens":not_found, 
                    "message":"Itens nao encontrados"
                }
            )

        new_receipe = receipe.to_mongoengine()

        new_receipe.items = [
            ItemWheight(item=item.id, wheight=item.wheight)
            for item in receipe.items
        ]

        receipe_db = self.receipe_repository.create(new_receipe)

        if not receipe_db:
            raise HTTPException(status_code=500, detail='Erro interno do servidor')
        
        return receipe_db.to_dict()
    
    def get_all_receipes(self):
        receipes_db = self.receipe_repository.get_all()

        if not receipes_db:
            raise HTTPException(status_code=404, detail=f'No receipes found')
        
        receipes = [receipe.to_dict() for receipe in receipes_db]
        return receipes
    
    def get_receipe_id(self, receipe_id: str):
        receipe = self.receipe_repository.get(receipe_id)
        if not receipe:
            raise HTTPException(status_code=404, detail=f'Product with ID: {receipe_id} not found')
        
        return receipe.to_dict()


def create_receipe_service():
    from src.repository.receipe_repository import ReceipeRepository
    from src.repository.item_repository import ItemRepository
    return ReceipeService(ReceipeRepository(), ItemRepository())

receipe_service = create_receipe_service()