from sqlalchemy.orm import Session

from app.core.errors import problem
from app.models.database import Exercise, Workout
from app.models.schemas import ExerciseCreate


def create_exercise(db: Session, exercise_data: ExerciseCreate, owner_id: int):
    workout = (
        db.query(Workout)
        .filter(Workout.id == exercise_data.workout_id, Workout.owner_id == owner_id)
        .first()
    )

    if not workout:
        return problem(
            status=404,
            title="Workout Not Found",
            detail="The requested workout was not found or access denied",
            instance=f"/workouts/{exercise_data.workout_id}",
        )

    db_exercise = Exercise(name=exercise_data.name, workout_id=exercise_data.workout_id)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def get_exercises(db: Session, owner_id: int):
    return db.query(Exercise).join(Workout).filter(Workout.owner_id == owner_id).all()


def get_exercises_by_workout(db: Session, workout_id: int, owner_id: int):
    return (
        db.query(Exercise)
        .join(Workout)
        .filter(Exercise.workout_id == workout_id, Workout.owner_id == owner_id)
        .all()
    )
