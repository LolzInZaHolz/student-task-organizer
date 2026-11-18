from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

BASE_DIR = Path(__file__).resolve().parent
COLOR_PATTERN = r"^#[0-9a-fA-F]{6}$"

app = FastAPI(
    title="Student Task Organizer API",
    version="0.1.0",
    description="Walking skeleton for the student task organizer.",
)


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


# In-memory store for the walking skeleton. Replaced by SQLite in Sprint 2.
courses_db: List[Course] = []


def _next_course_id() -> int:
    """Return an id that no current course uses."""
    return max((course.id for course in courses_db), default=0) + 1


@app.get("/", include_in_schema=False, response_class=FileResponse)
def index():
    """Serve the minimal Sprint 1 UI."""
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.post("/api/courses", response_model=Course, status_code=201)
def add_course(course: CourseCreate) -> Course:
    if not course.name:
        raise HTTPException(status_code=400, detail="Course name cannot be empty")
    if any(
        existing.name.casefold() == course.name.casefold()
        for existing in courses_db
    ):
        raise HTTPException(
            status_code=409,
            detail="A course with that name already exists",
        )

    new_course = Course(
        id=_next_course_id(),
        name=course.name,
        code=course.code,
        color=course.color,
    )
    courses_db.append(new_course)
    return new_course


@app.get("/api/courses", response_model=List[Course])
def get_courses() -> List[Course]:
    return courses_db


@app.get("/api/courses/{course_id}", response_model=Course)
def get_course(course_id: int) -> Course:
    for course in courses_db:
        if course.id == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")
