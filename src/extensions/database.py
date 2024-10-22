from mongoengine import connect, connection

from src.config import settings

def init_app(app):

    connect(db=settings.db_name, host=settings.db_host)

    if connection.get_connection().is_primary:
        print("MongoDB conectado")