"""EPIC-02: academic task management.

Member 2 owns this module in Sprint 1. Implement POST /api/tasks and the read
endpoints from the story issue. Use the shared Task model from ``models.py``
and the shared ``tasks_db`` from ``store.py``. Do not edit the other routers.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/tasks", tags=["tasks"])
