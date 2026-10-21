# needed even if not used
from backend.app.modules.shop_module import Shop
from backend.app.modules.item_module import Item
from backend.app.modules.shop_owner_module import ShopOwner
from backend.app.modules.item_category_module import ItemCategory

from sqlmodel import Session
from backend.app.database.db import engine

def create_shop_owner():
    with Session(engine) as session:
        shop_owner = ShopOwner(name="Skylah Rose")
        session.add(shop_owner)
        session.commit()
        session.refresh(shop_owner)
        return shop_owner

def create_shop():
    with Session(engine) as session:
        shop = Shop(name="Ankara Store", image="/images/ankarashop.png")
        session.add(shop)
        session.commit()
        session.refresh(shop)
        return shop
    
def create_category():
    with Session(engine) as session:
        category = ItemCategory(
            name = "clothes"
        )
        session.add(category)
        session.commit()
        session.refresh(category)
        return category

def create_item(shop_id: int, category_id: int):
    with Session(engine) as session:
        item = Item(
            name = "Akwaocha",
            price = 100,
            image = "/images/SneakerShopItems/akwaocha.png",
            description= "Hes the birthday, dont be the birthday planner",
            shop_id=shop_id,
            category_id=category_id
        )
        session.add(item)
        # save all changes to the database
        session.commit()
        # reload this object from the database so it has the latest values
        session.refresh(item)
        return item
    
if __name__ == "__main__":
    create_shop_owner()
    # create_shop()
    # create_category()
    # create_item(shop_id=1, category_id=1)
    print("Inserted data into table!")