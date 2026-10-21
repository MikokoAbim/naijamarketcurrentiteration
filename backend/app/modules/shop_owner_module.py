from sqlmodel import SQLModel, Field, Relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.modules.shop_module import Shop


class ShopOwner(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    shop: Shop = Relationship(back_populates="shop_owner")
