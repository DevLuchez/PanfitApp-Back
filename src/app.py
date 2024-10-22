from fastapi import FastAPI

from src.routes.receipe_routes import receipe_routes
from src.routes.product_routes import product_routes
from src.routes.item_routes import item_routes

from src.extensions import database

def create_app():
    app = FastAPI()
    app.include_router(item_routes)
    app.include_router(product_routes)
    app.include_router(receipe_routes)

    database.init_app(app)

    return app

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app=create_app(), host='127.0.0.1', port=5000)
