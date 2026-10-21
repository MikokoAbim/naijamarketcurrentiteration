from backend.app.modules.item_module import Item
from backend.app.database.db import engine
from sqlmodel import Session, select

def get_item_by_id(item_id: int) -> Item:
    """Get a specific item based on item_id """
    with Session(engine) as session:
        statement = select(Item).where(Item.id == item_id)
        item = session.exec(statement).first()
        print(item)
        return item