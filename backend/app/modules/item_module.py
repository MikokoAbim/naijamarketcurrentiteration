from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.modules.shop_module import Shop

class Item(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: int
    image: str | None = None
    description: str | None = None
    shop_id: int = Field(foreign_key="shop.id")

    shop: Optional["Shop"] = Relationship(back_populates="items")

