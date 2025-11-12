from sqlalchemy.orm import Session

from app.models.database import Exercise, Workout


def get_workouts_count(db: Session, owner_id: int):
    return db.query(Workout).filter(Workout.owner_id == owner_id).count()


def get_exercises_count(db: Session, owner_id: int):
    return db.query(Exercise).join(Workout).filter(Workout.owner_id == owner_id).count()


def get_last_workout(db: Session, owner_id: int):
    return (
        db.query(Workout)
        .filter(Workout.owner_id == owner_id)
        .order_by(Workout.date.desc())
        .first()
    )
