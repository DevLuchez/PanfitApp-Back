from fastapi import HTTPException
from datetime import datetime

from src.models.dto.item import ItemDTO

class ItemService:
    def __init__(self, item_repository):
        self.item_repository = item_repository

    def create_item(self, item_dto: ItemDTO):

        existing_item = list(self.item_repository.find(limit=1, GTIN=item_dto.GTIN))

        print(existing_item)
        
        if existing_item:

            updated_item = self.item_repository.update(
                item_id=existing_item[0]["_id"], 
                wheight=existing_item[0]["wheight"]+item_dto.wheight,
                updated_at=datetime.now()
            )

            if not updated_item:
                raise HTTPException(status_code=500, detail=f'Erro interno do servidor')
            
            return updated_item.to_dict()

        item_db = self.item_repository.create(item_dto.to_mongoengine())

        if not item_db:
            raise HTTPException(status_code=500, detail=f'Erro interno do servidor')
        
        return item_db.to_dict()
         
def create_item_service():
    from src.repository.item_repository import ItemRepository
    return ItemService(ItemRepository())

item_service = create_item_service()