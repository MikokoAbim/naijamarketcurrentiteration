from .db import engine
from sqlmodel import SQLModel

# 🔥 IMPORTANT: import all models so SQLModel registers them
from ..modules.shop_module import Shop
from ..modules.item_module import Item
from ..modules.shop_owner_module import ShopOwner
from ..modules.item_category_module import ItemCategory

def create_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db()
    print("Database tables created!")