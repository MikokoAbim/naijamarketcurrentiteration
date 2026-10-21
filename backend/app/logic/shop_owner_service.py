from sqlmodel import Session, select
from backend.app.database.db import engine
from backend.app.modules.shop_module import Shop
from backend.app.modules.item_module import Item
from backend.app.modules.shop_owner_module import ShopOwner
from sqlalchemy.orm import selectinload

def create_shop(shop: Shop):
    with Session(engine) as session:
        session.add(shop)
        session.commit()
        session.refresh(shop)
        return shop


def add_product_to_shop(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    
def get_shop_owner_by_id(shop_owner_id: int) -> ShopOwner:
    with Session(engine) as session:
        statement = select(ShopOwner).where(ShopOwner.id == shop_owner_id).options(selectinload(ShopOwner.shop))
        shop = session.exec(statement).first()
        return shop