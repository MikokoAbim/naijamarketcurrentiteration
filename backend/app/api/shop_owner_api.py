from fastapi import APIRouter
from backend.app.logic.shop_owner_service import create_shop, add_product_to_shop, get_shop_owner_by_id
from backend.app.modules.shop_module import Shop
from backend.app.modules.item_module import Item
from backend.app.non_table_modules.shop_owner_module import ShopOwnerWithShop

router = APIRouter()

@router.get("/{shop_owner_id}")
def api_get_shop_owner_by_id(shop_owner_id: int) -> ShopOwnerWithShop | None:
    return get_shop_owner_by_id(shop_owner_id)

@router.post("/create_shop")
def api_create_shop(shop: Shop):
    return create_shop(shop)

@router.post("/product_add")
def api_add_product_to_shop(item: Item):
    return add_product_to_shop(item)