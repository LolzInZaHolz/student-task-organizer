# Team playbook — Sprint 1 (walking skeleton)

**Rule for every sprint: one story per member.** Nobody owns an epic, and nobody takes
two stories in the same sprint. Each story is a thin vertical slice: router + page + tests.

| Member | Sprint 1 story | Issue | Branch |
| ------ | -------------- | ----- | ------ |
| 1 | 1.1 Add a course | [#3](../../issues/3) (done) | `feature/1-1-add-course` |
| 2 | 2.1 Add an assignment with due date and effort | [#4](../../issues/4) | `feature/2-1-add-task` |
| 3 | 3.1 Weekly calendar view | [#5](../../issues/5) | `feature/3-1-week-view` |
| 4 | 4.1 Warn when two exams fall on the same day | [#6](../../issues/6) | `feature/4-1-exam-clash` |

The Sprint 2 rule is the same: every member picks **one** unstarted story, and stories may
move to a different member than last sprint.

## Before you start (once per machine)

1. Accept the collaborator invite from the email or from
   `https://github.com/LolzInZaHolz/student-task-organizer/settings/access`.
2. Install Python 3.14 and Git.
3. Clone the repository:

   ```powershell
   cd C:\Users\<your-name>\Documents
   git clone https://github.com/LolzInZaHolz/student-task-organizer.git
   cd student-task-organizer
   ```

4. Create the environment and install dependencies:

   ```powershell
   py -3.14 -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

5. Check that the skeleton works:

   ```powershell
   pytest -q
   flake8 .
   uvicorn main:app --reload
   ```

   Open <http://127.0.0.1:8000>. Stop the server with `Ctrl+C`.

6. Tell Git who you are:

   ```powershell
   git config user.name "Your Name"
   git config user.email "you@example.com"
   ```

## The loop for every story

### 1. Claim the issue on GitHub

Open the story issue from the table above. In the right sidebar:

- **Assignees** → gear icon → select yourself.
- **Projects** → move the card to *In progress* (if the project board is enabled).

Read the acceptance criteria and the JSON contract before writing code.

### 2. Update `dev`

```powershell
git switch dev
git pull
```

`dev` is the integration branch. `main` only receives `dev` at the end of a sprint.

### 3. Create your branch

Use the branch name from the issue:

```powershell
git switch -c feature/2-1-add-task
```

### 4. Write the code in the files you own

Only touch the three files listed on your issue. The shared files are:

- `main.py` — app wiring and page routes (owned by Member 1)
- `models.py` — shared Pydantic models (owned by Member 1)
- `store.py` — shared in-memory lists (owned by Member 1)

If a shared file must change, comment on the issue instead of editing it. That is how the
four branches merge without conflicts.

### 5. Run everything locally

```powershell
pytest -q
flake8 .
uvicorn main:app --reload
```

Open your page, use it like a real student, and check the browser console for errors.

### 6. Commit in small steps

```powershell
git add routers/tasks.py static/tasks.html test_tasks.py
git commit -m "feat(tasks): add assignment creation endpoint and form"
```

Messages follow `type(scope): summary` — `feat`, `fix`, `test`, `docs`, `chore`.

### 7. Push

```powershell
git push -u origin feature/2-1-add-task
```

### 8. Open the pull request

GitHub prints a link after the push, or use the **Compare & pull request** banner on the
repository page. Then:

- **base:** `dev` (not `main`)
- **title:** the story number and a short summary, e.g. `2.1 Add assignment endpoint`
- **description:** what changed, how you tested it, and `Closes #4`
- **Reviewers:** gear icon → choose one teammate
- **Create pull request**

### 9. Wait for CI and the review

At the bottom of the PR page, the `lint-and-test` check runs flake8 and pytest. Click
**Details** to read a failure. Push more commits to the same branch to fix it — the check
runs again automatically.

The reviewer checks:

- the acceptance criteria are met;
- the happy path and at least one failure path are tested;
- no shared or unrelated files changed;
- no secrets, `venv/` or `__pycache__/` in the diff;
- `pytest -q` and `flake8 .` pass on their machine.

### 10. Merge and clean up

After the check is green and the review is approved:

1. **Squash and merge** → **Confirm squash and merge**.
2. **Delete branch**.
3. Locally:

   ```powershell
   git switch dev
   git pull
   git branch -d feature/2-1-add-task
   ```

## Member 2 — Story 2.1 (assignment)

**Issue:** [#4](../../issues/4) · **Files:** `routers/tasks.py`, `static/tasks.html`,
`test_tasks.py` · **Branch:** `feature/2-1-add-task`

### Backend skeleton

Replace the placeholder router with:

```python
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from models import Task, TaskCreate, TaskType
from store import courses_db, tasks_db

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def _next_task_id() -> int:
    return max((task.id for task in tasks_db), default=0) + 1


@router.post("", response_model=Task, status_code=201)
def add_task(task: TaskCreate) -> Task:
    if not any(course.id == task.course_id for course in courses_db):
        raise HTTPException(status_code=404, detail="Course not found")

    new_task = Task(id=_next_task_id(), **task.model_dump())
    tasks_db.append(new_task)
    return new_task


@router.get("", response_model=list[Task])
def get_tasks(
    course_id: Optional[int] = Query(default=None),
    task_type: Optional[TaskType] = Query(default=None, alias="type"),
) -> list[Task]:
    return [
        task
        for task in tasks_db
        if (course_id is None or task.course_id == course_id)
        and (task_type is None or task.type == task_type)
    ]


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")
```

`TaskCreate` already validates the title, date and positive effort. You only need the
course check and the id.

### Tests

`conftest.py` provides a `client` fixture and a `course` fixture that creates one course.

```python
def test_add_assignment(client, course):
    response = client.post(
        "/api/tasks",
        json={
            "course_id": course["id"],
            "title": "Database coursework",
            "type": "assignment",
            "due_date": "2026-11-20",
            "effort_hours": 4.0,
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["course_id"] == course["id"]
    assert body["effort_hours"] == 4.0
    assert body["completed"] is False


def test_task_requires_an_existing_course(client):
    response = client.post(
        "/api/tasks",
        json={
            "course_id": 999,
            "title": "Ghost task",
            "due_date": "2026-11-20",
            "effort_hours": 1.0,
        },
    )
    assert response.status_code == 404


def test_effort_must_be_positive(client, course):
    response = client.post(
        "/api/tasks",
        json={
            "course_id": course["id"],
            "title": "Zero effort",
            "due_date": "2026-11-20",
            "effort_hours": 0,
        },
    )
    assert response.status_code == 422
```

### Page

`static/tasks.html` already has the navigation and loads `style.css`. Add:

- a form with a course `<select>`, title, type, due date and effort;
- `fetch("/api/courses")` to fill the select;
- `POST /api/tasks` on submit, then re-render the list;
- an error paragraph using the `error` class, and an empty state.

### Manual check

1. `uvicorn main:app --reload`
2. Open `/tasks`.
3. Add an assignment with a real course, a date and 4 hours.
4. Check it appears in the list and in `/docs` under `GET /api/tasks`.

## Member 3 — Story 3.1 (week view)

**Issue:** [#5](../../issues/5) · **Files:** `routers/calendar.py`, `static/week.html`,
`test_calendar.py` · **Branch:** `feature/3-1-week-view`

### Backend skeleton

```python
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from models import Task
from store import courses_db, tasks_db

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


class CalendarTask(Task):
    course_name: str
    course_color: Optional[str] = None


class CalendarDay(BaseModel):
    date: date
    weekday: str
    tasks: list[CalendarTask]
    effort_hours: float


class WeekView(BaseModel):
    start: date
    end: date
    total_effort_hours: float
    days: list[CalendarDay]


def _monday_of_this_week() -> date:
    today = date.today()
    return today - timedelta(days=today.weekday())


@router.get("/week", response_model=WeekView)
def get_week(start: Optional[date] = Query(default=None)) -> WeekView:
    first_day = start or _monday_of_this_week()
    days = []

    for offset in range(7):
        day = first_day + timedelta(days=offset)
        day_tasks = []

        for task in tasks_db:
            if task.due_date != day:
                continue

            course = next(
                (course for course in courses_db if course.id == task.course_id),
                None,
            )
            day_tasks.append(
                CalendarTask(
                    **task.model_dump(),
                    course_name=course.name if course else "Unknown course",
                    course_color=course.color if course else None,
                )
            )

        days.append(
            CalendarDay(
                date=day,
                weekday=day.strftime("%A"),
                tasks=day_tasks,
                effort_hours=sum(task.effort_hours for task in day_tasks),
            )
        )

    return WeekView(
        start=first_day,
        end=first_day + timedelta(days=6),
        total_effort_hours=sum(day.effort_hours for day in days),
        days=days,
    )
```

`Optional[date]` makes FastAPI parse the query parameter; an invalid date returns `422`
without extra code.

### Tests

```python
def test_week_puts_tasks_on_the_right_day(client, course):
    client.post(
        "/api/tasks",
        json={
            "course_id": course["id"],
            "title": "Essay",
            "due_date": "2026-11-18",
            "effort_hours": 3.0,
        },
    )

    response = client.get("/api/calendar/week?start=2026-11-16")
    assert response.status_code == 200
    body = response.json()
    assert body["start"] == "2026-11-16"
    assert body["end"] == "2026-11-22"
    assert len(body["days"]) == 7
    assert body["days"][2]["weekday"] == "Wednesday"
    assert body["days"][2]["tasks"][0]["title"] == "Essay"
    assert body["total_effort_hours"] == 3.0


def test_week_is_empty_without_tasks(client):
    body = client.get("/api/calendar/week?start=2026-11-16").json()
    assert body["total_effort_hours"] == 0
    assert all(day["tasks"] == [] for day in body["days"])


def test_week_rejects_bad_date(client):
    assert client.get("/api/calendar/week?start=not-a-date").status_code == 422
```

### Page

`/week` should show:

- the date range;
- a large **total estimated effort** for the week (story 3.2 is included);
- seven cards, one per day, each listing title, course and hours;
- an empty state when nothing is due.

### Manual check

Create tasks across at least three days, then open `/week` and confirm they land on the
right day and the total equals the sum of the hours.

## Member 4 — Story 4.1 (exam clash)

**Issue:** [#6](../../issues/6) · **Files:** `routers/warnings.py`, `static/warnings.html`,
`test_warnings.py` · **Branch:** `feature/4-1-exam-clash`

### Backend skeleton

```python
from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel

from models import Task, TaskType
from store import courses_db, tasks_db

router = APIRouter(prefix="/api/warnings", tags=["warnings"])


class WarningTask(BaseModel):
    id: int
    title: str
    course_name: str


class Warning(BaseModel):
    type: str
    date: date
    message: str
    tasks: list[WarningTask]


class WarningList(BaseModel):
    warnings: list[Warning]


def _course_name(course_id: int) -> str:
    course = next((course for course in courses_db if course.id == course_id), None)
    return course.name if course else "Unknown course"


@router.get("", response_model=WarningList)
def get_warnings() -> WarningList:
    exams_by_date: dict[date, list[Task]] = {}

    for task in tasks_db:
        if task.type == TaskType.exam:
            exams_by_date.setdefault(task.due_date, []).append(task)

    warnings = []
    for exam_date in sorted(exams_by_date):
        exams = exams_by_date[exam_date]
        if len(exams) < 2:
            continue

        warnings.append(
            Warning(
                type="exam_clash",
                date=exam_date,
                message=f"{len(exams)} exams on {exam_date.isoformat()}",
                tasks=[
                    WarningTask(
                        id=exam.id,
                        title=exam.title,
                        course_name=_course_name(exam.course_id),
                    )
                    for exam in exams
                ],
            )
        )

    return WarningList(warnings=warnings)
```

### Tests

```python
def add_exam(client, course, title, due_date):
    response = client.post(
        "/api/tasks",
        json={
            "course_id": course["id"],
            "title": title,
            "type": "exam",
            "due_date": due_date,
            "effort_hours": 2.0,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_two_exams_on_the_same_day(client, course):
    add_exam(client, course, "Databases final", "2026-12-10")
    add_exam(client, course, "Algorithms final", "2026-12-10")

    body = client.get("/api/warnings").json()
    assert len(body["warnings"]) == 1
    warning = body["warnings"][0]
    assert warning["type"] == "exam_clash"
    assert warning["date"] == "2026-12-10"
    assert len(warning["tasks"]) == 2


def test_one_exam_is_not_a_clash(client, course):
    add_exam(client, course, "Databases final", "2026-12-10")
    assert client.get("/api/warnings").json()["warnings"] == []


def test_assignments_are_ignored(client, course):
    for title in ("Essay", "Lab report"):
        client.post(
            "/api/tasks",
            json={
                "course_id": course["id"],
                "title": title,
                "due_date": "2026-12-10",
                "effort_hours": 3.0,
            },
        )

    assert client.get("/api/warnings").json()["warnings"] == []
```

### Page

`/warnings` should show one card per clash with the date, the message and the exam titles,
and a clear positive state when there are no clashes.

### Manual check

Add two exams on the same date, open `/warnings`, confirm one warning with both exams.
Delete one exam from the store or use a different date and confirm the warning disappears.

## Member 1 — Story 1.1 and integration

Story 1.1 is delivered. For the rest of Sprint 1 you are the integration owner:

- keep `dev` green and review every PR within one working day;
- run the PR branch locally before approving;
- resolve shared-file changes (only you edit `main.py`, `models.py`, `store.py`);
- merge `dev` into `main` at the end of the sprint;
- run the demo.

Review checklist:

- [ ] all acceptance criteria on the issue are met;
- [ ] tests cover success and failure;
- [ ] only the three owned files changed;
- [ ] `pytest -q` and `flake8 .` pass locally;
- [ ] the page works and has an empty state;
- [ ] no `venv/`, cache folders or secrets in the diff.

## Integration rules

- **Contract first.** The `Course` and `Task` shapes in `README.md` are the source of
  truth. Do not rename fields without a team decision.
- **Ids** come from `max(existing id) + 1`, never `len(list) + 1`.
- **Errors:** `400` for a blank required text field, `404` for a missing parent, `409`
  for a duplicate, `422` for schema validation.
- **Dates** are ISO `YYYY-MM-DD` strings in JSON. Effort is a number of hours.
- **Never push to `main` or `dev`.** Branch protection rejects it; use a PR.
- **One story per PR.** If you notice an unrelated bug, open an issue instead of fixing it
  in the same PR.
- **If `dev` moved while you worked:**

  ```powershell
  git fetch origin
  git rebase origin/dev
  git push --force-with-lease
  ```

  Resolve conflicts in your own files if possible.

## Sprint 1 demo script (5 minutes)

Run the demo in dependency order:

1. **Member 1** — add two courses with different colours on `/`, show the list.
2. **Member 2** — add an assignment due Wednesday (3 h) and an exam due Thursday (2 h) on
   `/tasks`.
3. **Member 3** — open `/week`, show both tasks on the right days and a total of 5 h.
4. **Member 4** — add a second exam on Thursday, open `/warnings`, show the clash.
5. **Member 1** — show the green PR checks and the Actions tab, then the `dev` to `main`
   release PR.

## When something goes wrong

| Symptom | Fix |
| ------- | --- |
| `git push` rejected on `dev`/`main` | You are on a protected branch. Create `feature/...` and open a PR. |
| CI red, local green | Check the Python version (3.14) and that `requirements.txt` is unchanged. Click **Details** for the log. |
| `ModuleNotFoundError` | Activate the venv: `.\venv\Scripts\Activate.ps1`, then `pip install -r requirements.txt`. |
| Merge conflict | You edited a file you do not own. Ask the owner in the PR, or rebase and keep their version. |
| Test sees data from another test | `conftest.py` clears both stores automatically; do not create your own global lists. |
