from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Student Task Organizer API")


# Data model for a Course
class CourseCreate(BaseModel):
    name: str
    code: Optional[str] = None


class Course(CourseCreate):
    id: int


# In-memory database for the Walking Skeleton
courses_db: List[Course] = []


@app.post("/api/courses", response_model=Course, status_code=201)
def add_course(course: CourseCreate):
    if not course.name.strip():
        raise HTTPException(status_code=400, detail="Course name cannot be empty")
    new_course = Course(
        id=len(courses_db) + 1,
        name=course.name,
        code=course.code
    )
    courses_db.append(new_course)
    return new_course


@app.get("/api/courses", response_model=List[Course])
def get_courses():
    return courses_db
    