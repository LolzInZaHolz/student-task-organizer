# Week 5 — Before and after

Measured on the same machine, same Python (3.14.7) and same tools
(Ruff 0.17.6, Pylint 4.1.4). The "before" column comes from the untouched
`week5/legacy_fees.py` (raw output in [`before.txt`](before.txt)); the "after"
column comes from `week5/fees.py` after all seven refactoring steps.

## The table

| Measure | Before (`legacy_fees.py`) | After (`fees.py`) |
| --- | --- | --- |
| Ruff issues (total) | 17 | **0** |
| Highest cyclomatic complexity | 9 (`calc`) | **4** (`tuition_fee`) |
| Arguments of the main function | 6 | **5** (3 required, 2 keyword with defaults) |
| Pylint score (/10) | 4.86 | 10.00 |
| Tests passing | 0 — no tests existed for the legacy code | **26** (15 kata + 11 fees) |

Commands used for the "after" column, run from inside `week5/`:

```text
python -m pytest -q     ->  26 passed
ruff check .            ->  All checks passed!
pylint fees.py          ->  Your code has been rated at 10.00/10
ruff check --select C901 --config "lint.mccabe.max-complexity=1" fees.py
                        ->  tuition_fee (4), report (2), process_all (2)
```

The last command proves the complexity drop: with the threshold forced down to
1, the worst function in the new file scores 4 instead of 9.

## What each step removed

| Step | Commit | Rule / smell removed |
| --- | --- | --- |
| 1 | `refactor: step 1 port calc into fees.py and delete dead code` | F401 ×2, F841, ARG001 |
| 2 | `refactor: step 2 rename the remaining cryptic locals` | mysterious names (`c`, `e`, `st`, `x`) |
| 3 | `refactor: step 3 replace magic numbers with named constants and a StudentType enum` | PLR2004 ×6, the type-code comment |
| 4 | `refactor: step 4 replace the if/elif chain with a rate table` | C901, E711, E712 |
| 5 | `refactor: step 5 use an immutable extras default` | B006 |
| 6 | `refactor: step 6 separate calculation from printing` | mixed responsibilities in `report` |
| 7 | `fix: step 7 give every student a fee, including scholarships` | the hidden bug in `process_all` |

Two honest notes on the order:

- **Steps 1 and 2 overlap slightly.** The characterization tests in
  `test_fees.py` describe the *target* API (`tuition_fee`, `Course`,
  `StudentType`, `process_all`), so those public names had to exist from step 1
  for the tests to import at all. Step 2 then renamed what was left inside the
  functions.
- **The `Course` dataclass arrived with step 1, not step 5.** The tests construct
  `Course(3)` from the first commit, and a frozen dataclass is the smallest thing
  that makes that possible without changing the arithmetic.

## Does 100% coverage prove the code is correct?

*(not part of this lab — see `docs/lab6/` — but the same reasoning applies here)*
No: coverage says which lines ran, not whether the expected values were right.

## Pairing reflection

The pair worked the three rounds on one keyboard with a 12-minute timer:
Abdullah Hesham drove round 1 (the failing tests, then `letter_grade`), Ahmed
Ramez navigated and then drove round 2 (the boundary list), and Eyad Mohamed
navigated round 3 (the magic-number refactor) while Nour Ezz El Deen and Ahmed
Elgendy reviewed each diff at the end of a round and kept the task list.
The navigator wrote the characterization tests, because describing today's
behaviour turned out to be harder than writing new code, and a second pair of
eyes on the arithmetic (6300 − 200 = 6100, 18 h plus summer = 6250) caught two
wrong expected values before they reached a commit.
The lesson was that the tools were the cheap part — Ruff and Pylint said *where*
to look in seconds — while the expensive part was deciding whether a change was
really behaviour-preserving, which is exactly what the characterization tests
were for.
Pairing cost us roughly the 15% extra effort the lecture mentions, and it paid
for itself immediately: the hidden bug in `ProcessAll` was found by a person
reading the loop, not by any linter.
