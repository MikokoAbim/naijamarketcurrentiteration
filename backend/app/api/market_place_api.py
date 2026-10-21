from fastapi import APIRouter
from backend.app.logic.market_place_service import get_market_place, get_shop_by_id, get_shop_by_name
from backend.app.modules.market_place_module import MarketPlace
from backend.app.modules.shop_module import Shop
from backend.app.non_table_modules.shop_module import ShopWithItems

router = APIRouter()

@router.get("/")
def api_get_market_place() -> MarketPlace:
    return get_market_place()

@router.get("/shops/by-name")
def api_get_shop_by_name(name: str) -> list[Shop] | None:
    return get_shop_by_name(name)

@router.get("/shops/{shop_id}")
def api_get_shop_by_id(shop_id: int) -> ShopWithItems | None:
    return get_shop_by_id(shop_id)
