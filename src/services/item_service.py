from fastapi import HTTPException

from src.models.dto.item import ItemDTO

class ItemService:
    def __init__(self, item_repository):
        self.item_repository = item_repository

    def create_item(self, item: ItemDTO):
        item_db = self.item_repository.create(item.to_mongoengine())

        if not item_db:
            raise HTTPException(status_code=500, detail=f'Erro interno do servidor')
        
        return item_db.to_dict()
         
def create_item_service():
    from src.repository.item_repository import ItemRepository
    return ItemService(ItemRepository())

item_service = create_item_service()