from pydantic import BaseModel
from backend.app.modules.shop_module import Shop

class MarketPlace(BaseModel):
    shops: list[Shop]