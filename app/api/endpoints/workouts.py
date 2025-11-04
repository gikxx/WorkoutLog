from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.core.errors import problem
from app.models.schemas import WorkoutCreate, WorkoutResponse
from app.services.workout_service import WorkoutService

router = APIRouter()


@router.post("/", response_model=WorkoutResponse)
def create_workout(
    workout: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    service = WorkoutService(db)
    db_workout = service.create_workout(workout, current_user_id)
    return db_workout


@router.get("/", response_model=list[WorkoutResponse])
def get_workouts(
    db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)
):
    service = WorkoutService(db)
    return service.get_workouts(current_user_id)


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    service = WorkoutService(db)
    workout = service.get_workout_by_id(workout_id, current_user_id)
    if not workout:
        return problem(
            status=status.HTTP_404_NOT_FOUND,
            title="Workout Not Found",
            detail="The requested workout was not found",
            instance=f"/workouts/{workout_id}",
        )
    return workout
