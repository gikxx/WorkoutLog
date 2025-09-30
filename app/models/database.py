from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    workouts = relationship(
        "Workout", back_populates="owner", cascade="all, delete-orphan"
    )


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    note = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="workouts")
    exercises = relationship(
        "Exercise", back_populates="workout", cascade="all, delete-orphan"
    )


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)

    # Relationships
    workout = relationship("Workout", back_populates="exercises")
    sets = relationship("Set", back_populates="exercise", cascade="all, delete-orphan")


class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, index=True)
    reps = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)

    # Relationships
    exercise = relationship("Exercise", back_populates="sets")
