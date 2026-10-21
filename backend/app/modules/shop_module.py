from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.modules.item_module import Item
    from backend.app.modules.shop_owner_module import ShopOwner
    

class Shop(SQLModel, table = True):
    id: int| None = Field(default=None, primary_key=True)
    name: str
    image: str | None = None
    shop_owner_id: int = Field(foreign_key="shopowner.id")

    shop_owner: ShopOwner = Relationship(back_populates="shop")
    items: list["Item"] = Relationship(back_populates="shop")