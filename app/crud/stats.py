from sqlalchemy.orm import Session

from app.models.database import Exercise, Workout


def get_workouts_count(db: Session):
    return db.query(Workout).count()


def get_exercises_count(db: Session):
    return db.query(Exercise).count()


def get_last_workout(db: Session):
    return db.query(Workout).order_by(Workout.date.desc()).first()
