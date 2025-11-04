import html
import re
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UserBase(BaseModel):
    email: str = Field(
        min_length=5,
        max_length=100,
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        examples=["user@example.com"],
    )


class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=100,
        pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$",
        description="Password must contain uppercase, lowercase and numbers",
    )


class WorkoutBase(BaseModel):
    note: Optional[str] = Field(
        None,
        max_length=500,
        pattern=r"^[a-zA-Z0-9\s\.,!?\-_]+$",
        description="Workout note can only contain letters, numbers, and basic punctuation",
    )

    @field_validator("note")
    @classmethod
    def sanitize_note(cls, v):
        if v:
            if not re.match(r"^[a-zA-Z0-9\s\.,!?\-_]+$", v):
                raise ValueError("Note contains invalid characters")
            return html.escape(v.strip())
        return v


class ExerciseBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[a-zA-Z0-9\s\-_]+$",
        examples=["Bench Press", "Squat"],
    )

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, v):
        if v:
            if not re.match(r"^[a-zA-Z0-9\s\-_]+$", v):
                raise ValueError(
                    "Name can only contain letters, numbers, spaces, hyphens and underscores"
                )
            return html.escape(v.strip())
        return v


class SetBase(BaseModel):
    reps: int = Field(gt=0, le=100, description="Reps must be between 1 and 100")
    weight: Decimal = Field(
        gt=0, le=500, max_digits=5, decimal_places=2, examples=[67.5, 100.0]
    )

    @field_validator("weight")
    @classmethod
    def validate_weight_precision(cls, v):
        if v is not None:
            return round(v, 2)
        return v
