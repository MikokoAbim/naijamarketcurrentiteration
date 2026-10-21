from sqlmodel import SQLModel
from backend.app.modules.item_module import Item
from backend.app.modules.shop_owner_module import ShopOwner

class ShopWithItems(SQLModel):
    id: int
    name: str
    image: str | None = None
    shop_owner: ShopOwner
    items: list[Item] = []