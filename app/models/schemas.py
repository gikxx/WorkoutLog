import html
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# User Schemas
class UserBase(BaseModel):
    email: str = Field(
        min_length=5, max_length=100, description="Email must be 5-100 characters"
    )


class UserCreate(UserBase):
    password: str = Field(
        min_length=8, max_length=100, description="Password must be 8-100 characters"
    )


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Workout Schemas
class WorkoutBase(BaseModel):
    note: Optional[str] = Field(
        None, max_length=500, description="Workout note max 500 characters"
    )

    @field_validator("note")
    @classmethod
    def sanitize_note(cls, v):
        if v:
            return html.escape(v.strip())
        return v


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutResponse(WorkoutBase):
    id: int
    date: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


# Exercise Schemas
class ExerciseBase(BaseModel):
    name: str = Field(
        min_length=1, max_length=100, description="Exercise name 1-100 characters"
    )

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, v):
        if v:
            return html.escape(v.strip())
        return v


class ExerciseCreate(ExerciseBase):
    workout_id: int = Field(gt=0, description="Workout ID must be positive integer")


class ExerciseResponse(ExerciseBase):
    id: int
    workout_id: int

    model_config = ConfigDict(from_attributes=True)


# Set Schemas
class SetBase(BaseModel):
    reps: int = Field(gt=0, le=100, description="Reps must be between 1 and 100")
    weight: float = Field(
        gt=0, le=500, description="Weight must be between 0.1 and 500 kg"
    )

    @field_validator("weight")
    @classmethod
    def validate_weight_precision(cls, v):
        if v is not None and round(v, 2) != v:
            raise ValueError("Weight must have maximum 2 decimal places")
        return round(v, 2) if v is not None else v


class SetCreate(SetBase):
    exercise_id: int = Field(gt=0, description="Exercise ID must be positive integer")


class SetResponse(SetBase):
    id: int
    exercise_id: int

    model_config = ConfigDict(from_attributes=True)
