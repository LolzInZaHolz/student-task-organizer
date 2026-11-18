from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routers import calendar, courses, tasks, warnings

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Student Task Organizer API",
    version="0.1.0",
    description="Walking skeleton for the student task organizer.",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(courses.router)
app.include_router(tasks.router)
app.include_router(calendar.router)
app.include_router(warnings.router)


def _page(name: str) -> FileResponse:
    return FileResponse(BASE_DIR / "static" / f"{name}.html")


@app.get("/", include_in_schema=False, response_class=FileResponse)
def index():
    """Course page (Member 1)."""
    return _page("index")


@app.get("/tasks", include_in_schema=False, response_class=FileResponse)
def tasks_page():
    """Task page (Member 2)."""
    return _page("tasks")


@app.get("/week", include_in_schema=False, response_class=FileResponse)
def week_page():
    """Weekly calendar page (Member 3)."""
    return _page("week")


@app.get("/warnings", include_in_schema=False, response_class=FileResponse)
def warnings_page():
    """Warnings page (Member 4)."""
    return _page("warnings")
