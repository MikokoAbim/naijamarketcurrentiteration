from fastapi import APIRouter
from backend.app.modules.item_module import Item
from backend.app.logic.item_service import get_item_by_id

router = APIRouter()


@router.get("/{item_id}")
def api_get_item_details(item_id: int) -> Item:
    return get_item_by_id(item_id)