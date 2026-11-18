"""EPIC-04: deadline warnings.

Member 4 owns this module in Sprint 1. Implement GET /api/warnings from the
story issue. Read tasks from ``store.tasks_db``. Do not edit the other routers.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/warnings", tags=["warnings"])
