from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.schemas import ExerciseCreate, ExerciseResponse
from app.services.exercise_service import ExerciseService

router = APIRouter()


@router.post("/", response_model=ExerciseResponse)
def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    service = ExerciseService(db)
    db_exercise = service.create_exercise(exercise, current_user_id)
    return db_exercise


@router.get("/", response_model=list[ExerciseResponse])
def get_exercises(
    db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)
):
    service = ExerciseService(db)
    return service.get_exercises(current_user_id)
