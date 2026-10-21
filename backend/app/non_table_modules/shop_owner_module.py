from sqlmodel import SQLModel
from backend.app.modules.shop_module import Shop

class ShopOwnerWithShop(SQLModel):
    id: int
    name: str
    shop: Shop | None = None