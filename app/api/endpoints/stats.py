from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.services.stats_service import StatsService

router = APIRouter()


@router.get("/")
def get_stats(
    db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)
):
    service = StatsService(db)
    return service.get_stats(current_user_id)
