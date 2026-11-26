# Part C - Smells and refactoring

## Task C1: smells in `legacy_invoice.py`

| Smell | Where | Principle it breaks |
| --- | --- | --- |
| Long `if`/`elif` chain on `kind` | Loop body and after the loop | OCP: a new student type means editing this function |
| One function calculates, formats, writes a file and prints | The whole of `make_invoice` | SRP: several reasons to change |
| File path and `open()` hard-coded inside the logic | The three file lines | DIP: depends on the disk, not on "something with `write()`" |
| Magic numbers `1200`, `0.5`, `2000`, `5000` (`1200` repeated) | Fee calculation | Readability and DRY |
| File opened without `with` | `f = open(...)` | Resource safety: the file stays open if `write` fails |
| Fee worked out course by course, though only total hours matter | The `for` loop | KISS: repeats what `Student.total_hours` already does |

## Refactoring moves

| Move | Change | Principle |
| --- | --- | --- |
| 1 | Characterization tests, passing on the unchanged code | Safety net |
| 2 | Named the magic numbers | Readability |
| 3 | One policy class per fee rule | SRP |
| 4 | `POLICIES` lookup instead of `if`/`elif` | OCP |
| 5 | File writer passed in as a parameter | DIP |
| C2 | `SiblingPolicy` (25% off the regular fee), test first | `make_invoice` unchanged |

## Before and after (measured)

| Measure | Before | After |
| --- | --- | --- |
| Cyclomatic complexity of `make_invoice` (Ruff C901) | 6 | 1 |
| Tests passing (`python -m pytest -q`) | 8 | 10 (fake-writer test and sibling test added) |
| Add a new fee type | Edit the function's `if`/`elif` chain | Add one class and one dictionary entry |
| Test without writing files | Not possible without redirecting the disk | Yes, with `FakeWriter` |

The "before" count is 8 (5 registration tests and 3 invoice tests). The handout shows
7 because it was measured without the fifth registration test.

## Behaviour changes (both follow the handout's model solution)

- `make_invoice` no longer prints the invoice; showing it is the caller's job.
- An unknown `kind` now raises `KeyError`. The old code wrote an invoice for 0 EGP.
