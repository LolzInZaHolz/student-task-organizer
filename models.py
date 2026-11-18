from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator

COLOR_PATTERN = r"^#[0-9a-fA-F]{6}$"


class CourseCreate(BaseModel):
    """Payload accepted when registering a new course."""

    name: str = Field(max_length=100, examples=["Software Engineering"])
    code: Optional[str] = Field(default=None, max_length=20, examples=["CS301"])
    color: Optional[str] = Field(
        default=None,
        pattern=COLOR_PATTERN,
        examples=["#2563EB"],
        description="Hex colour used to tell courses apart on the calendar.",
    )

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("code")
    @classmethod
    def normalise_code(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip() or None


class Course(CourseCreate):
    id: int


class TaskType(str, Enum):
    assignment = "assignment"
    exam = "exam"


class TaskCreate(BaseModel):
    """Payload accepted when adding an assignment or an exam."""

    course_id: int = Field(gt=0, examples=[1])
    title: str = Field(max_length=200, examples=["Database coursework"])
    type: TaskType = TaskType.assignment
    due_date: date = Field(examples=["2026-11-20"])
    effort_hours: float = Field(gt=0, le=100, examples=[4.0])
    completed: bool = False

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Task title cannot be empty")
        return value


class Task(TaskCreate):
    id: int
