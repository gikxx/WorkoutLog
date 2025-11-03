from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.schemas import WorkoutCreate, WorkoutResponse
from app.services.workout_service import WorkoutService

router = APIRouter()


@router.post("/", response_model=WorkoutResponse)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    service = WorkoutService(db)
    db_workout = service.create_workout(workout)
    return db_workout


@router.get("/", response_model=list[WorkoutResponse])
def get_workouts(db: Session = Depends(get_db)):
    service = WorkoutService(db)
    return service.get_workouts()


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    service = WorkoutService(db)
    workout = service.get_workout_by_id(workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout
