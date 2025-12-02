from fastapi import APIRouter
import structlog
from app.services import item_service
from app.models.item import Item

router = APIRouter()
log = structlog.get_logger()


@router.get("/items", response_model=list[Item])
def read_items():
    """
    Retrieve all items.
    """
    log.info("Fetching all items from the service")
    items = item_service.get_all_items()
    log.info("Retrieved items", item_count=len(items))
    return items