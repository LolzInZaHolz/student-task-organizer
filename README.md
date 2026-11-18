# Student Task Organizer

A student planner built as a course project: register your courses, add assignments and
exams with due dates and estimated effort, then see the week ahead and get warned when
your workload is unrealistic.

The repository is currently at the **Sprint 1 walking skeleton** stage: the thinnest
end-to-end slice (browser &rarr; API &rarr; store) plus a CI pipeline that lints and tests
every pull request.

## What works today

- Add a course, with an optional hex colour
- List all registered courses
- Fetch a single course
- A minimal web page for adding and listing courses
- pytest suite and flake8, both enforced by GitHub Actions

## Quick start

Requires Python 3.14 (the same version CI uses).

```powershell
py -3.14 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

- Web UI: <http://127.0.0.1:8000>
- Interactive API docs: <http://127.0.0.1:8000/docs>

## Tests and lint

```powershell
pytest -q
flake8 .
```

Both commands must pass before a pull request is merged.

## API

| Method | Path                | Purpose              | Responses                          |
| ------ | ------------------- | -------------------- | ---------------------------------- |
| GET    | `/`                 | Sprint 1 web page    | 200                                |
| POST   | `/api/courses`      | Register a course    | 201 · 400 · 409 · 422              |
| GET    | `/api/courses`      | List courses         | 200                                |
| GET    | `/api/courses/{id}` | Fetch one course     | 200 · 404                          |

### Course contract

```json
{
  "id": 1,
  "name": "Software Engineering",
  "code": "CS301",
  "color": "#2563EB"
}
```

- `name` is required, trimmed, and must be unique (case-insensitive). Empty names return
  `400`; duplicates return `409`.
- `code` is optional; blank strings are stored as `null`.
- `color` is optional and must be a six-digit hex value such as `#2563EB`.
- `id` is generated from the highest existing id, so deleting a course never causes a
  later course to reuse an id.

### Shared contract for the task stories

Members 2, 3 and 4 can build against this now, before the endpoint exists:

```json
{
  "id": 1,
  "course_id": 1,
  "title": "Database coursework",
  "type": "assignment",
  "due_date": "2026-11-20",
  "effort_hours": 4.0,
  "completed": false
}
```

`type` is `"assignment"` or `"exam"`; `due_date` is ISO `YYYY-MM-DD`.

## Project structure

```text
.
├── .github/workflows/ci.yml   # lint + test on every push and pull request
├── .flake8                    # linter configuration
├── .gitignore
├── main.py                    # FastAPI app and course endpoints
├── requirements.txt           # pinned dependencies (CI uses the same file)
├── static/index.html          # minimal Sprint 1 UI, no build step
├── test_main.py               # pytest suite
└── README.md
```

## Branching and CI

| Branch            | Purpose                                            |
| ----------------- | -------------------------------------------------- |
| `main`            | Always demoable; merged from `dev` at a review     |
| `dev`             | Integration branch; all feature PRs land here      |
| `feature/<story>` | One story per branch, deleted after merge          |

1. Branch from `dev`.
2. Commit in small steps.
3. Push and open a pull request into `dev`.
4. GitHub Actions runs flake8 and pytest; the `lint-and-test` check must be green.
5. One teammate reviews, then the PR is squash-merged.
6. At the end of the sprint, `dev` is merged into `main`.

Branch protection on `main` and `dev` requires the `lint-and-test` check, so a red build
cannot be merged.

## Sprint allocation (4 members)

| Member | Owns    | Sprint 1 (skeleton)               | Sprint 2 (core)                   | Sprint 3 (stretch)     |
| ------ | ------- | --------------------------------- | --------------------------------- | ---------------------- |
| 1      | EPIC-01 | Add a course                      | View the course list              | Course colour          |
| 2      | EPIC-02 | Add an assignment (due + effort)  | Add an exam · edit effort         | —                      |
| 3      | EPIC-03 | Weekly calendar view              | Weekly total effort               | Import class schedule  |
| 4      | EPIC-04 | Same-day exam warning             | More than three deadlines / 2 days| Push and email reminders |

The Sprint 1 stories form one end-to-end flow: create a course &rarr; add work under it
&rarr; see the week &rarr; receive a warning. Each member owns one epic so parallel work
does not collide.

## Definition of done

A story is done when:

- the endpoint (or screen) behaves as described in its acceptance criteria;
- tests cover the happy path and at least one failure path;
- `flake8 .` and `pytest -q` both pass locally;
- CI is green on the pull request and a teammate has reviewed it;
- the README is updated if the API changed;
- the change can be shown in the sprint demo.

## Roadmap

- **Sprint 2:** tasks and exams, week view totals, SQLite persistence, module split.
- **Sprint 3:** clash and overload warnings, course colour, schedule import, reminders.
