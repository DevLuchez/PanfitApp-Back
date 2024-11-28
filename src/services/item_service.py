from fastapi import HTTPException
from datetime import datetime

from src.models.dto.item import ItemDTO

class ItemService:
    def __init__(self, item_repository):
        self.item_repository = item_repository

    def create_item(self, item_dto: ItemDTO):

        existing_item = self.item_repository.get(GTIN=item_dto.GTIN)

        print(existing_item)
        
        if existing_item:

            updated_item = self.item_repository.update(
                item_id=existing_item.id, 
                stock_wheight=existing_item.stock_wheight+item_dto.wheight,
                updated_at=datetime.now()
            )

            if not updated_item:
                raise HTTPException(status_code=500, detail=f'Erro interno do servidor')
            
            return updated_item.to_dict()

        item_db = self.item_repository.create(item_dto.to_mongoengine())

        if not item_db:
            raise HTTPException(status_code=500, detail=f'Erro interno do servidor')
        
        return item_db.to_dict()
    
    def get_all_items(self):

        items_db = self.item_repository.get_all()
        if not items_db:
            raise HTTPException(status_code=404, detail=f'No items found')
        
        item_dict = [item.to_dict() for item in items_db]
        
        return item_dict

    def get_item_by_id(self, item_id: str):

        item = self.item_repository.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f'Item not found')
        
        return item.to_dict()
         
def create_item_service():
    from src.repository.item_repository import ItemRepository
    return ItemService(ItemRepository())

item_service = create_item_service()