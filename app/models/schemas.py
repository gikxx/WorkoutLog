from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# User Schemas
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Workout Schemas
class WorkoutBase(BaseModel):
    note: Optional[str] = None


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutResponse(WorkoutBase):
    id: int
    date: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


# Exercise Schemas
class ExerciseBase(BaseModel):
    name: str


class ExerciseCreate(ExerciseBase):
    workout_id: int


class ExerciseResponse(ExerciseBase):
    id: int
    workout_id: int

    model_config = ConfigDict(from_attributes=True)


# Set Schemas
class SetBase(BaseModel):
    reps: int
    weight: float


class SetCreate(SetBase):
    exercise_id: int


class SetResponse(SetBase):
    id: int
    exercise_id: int

    model_config = ConfigDict(from_attributes=True)
