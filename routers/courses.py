from fastapi import APIRouter, HTTPException

from models import Course, CourseCreate
from store import courses_db

router = APIRouter(prefix="/api/courses", tags=["courses"])


def _next_course_id() -> int:
    """Return an id that no current course uses."""
    return max((course.id for course in courses_db), default=0) + 1


@router.post("", response_model=Course, status_code=201)
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


@router.get("", response_model=list[Course])
def get_courses() -> list[Course]:
    return courses_db


@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int) -> Course:
    for course in courses_db:
        if course.id == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")
