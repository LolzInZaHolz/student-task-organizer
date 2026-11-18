"""EPIC-03: calendar and workload.

Member 3 owns this module in Sprint 1. Implement GET /api/calendar/week from the
story issue. Read tasks from ``store.tasks_db`` and courses from
``store.courses_db``. Do not edit the other routers.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/calendar", tags=["calendar"])
