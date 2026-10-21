from backend.app.modules.market_place_module import MarketPlace
from backend.app.modules.shop_module import Shop
from backend.app.modules.item_module import Item
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from backend.app.database.db import engine


def get_all_shops() -> list[Shop]:
    """Get all shops available in the marketplace"""
    with Session(engine) as session:
        shops = session.exec(select(Shop)).all()
        return shops

def get_shop_by_id(shop_id: int) -> Shop | None:
    """Get a specific shop based on shop_id"""
    with Session(engine) as session:
        # the selectinload is necessary because if we use a basic get, items within Shop will not be accessible
        # because relationships are lazy loaded and need to be explicitly asked for
        statement = select(Shop).where(Shop.id == shop_id).options(selectinload(Shop.items), selectinload(Shop.shop_owner))
        shop = session.exec(statement).first()
        # print(shop.items)
        return shop
    
def get_shop_by_name(shop_name: str) -> list[Shop] | None:
    """Get a specific shop based on shop_name"""
    with Session(engine) as session:
        statement = select(Shop).where(Shop.name == shop_name)
        shops = session.exec(statement).all()
        return shops

def get_market_place() -> MarketPlace:
    """Get the Marketplace object which contains the list of shops"""
    return MarketPlace(shops = get_all_shops())