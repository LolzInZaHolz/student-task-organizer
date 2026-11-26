# Lab 6 - TDD, BDD and refactoring

| What to submit | Where |
| --- | --- |
| Git log, one commit per TDD cycle | [`git_log.txt`](git_log.txt); red and green runs in [`tdd_log.txt`](tdd_log.txt) |
| Coverage at 100% and one-sentence answer | [`coverage.md`](coverage.md), `coverage.png`, `coverage_report.txt` |
| Feature file with drop scenario, `behave` all green | [`registration.feature`](../../lab6/features/registration.feature), `behave_output.txt` |
| Smells table and `invoice.py` with `SiblingPolicy` | [`smells.md`](smells.md), [`invoice.py`](../../lab6/invoice.py) |
| Three Gherkin scenarios for the team story | [`team_story_scenarios.md`](team_story_scenarios.md) |

`coverage.png`, `coverage_report.txt` and `behave_output.txt` are added after running
the tools locally.

Run everything from the `lab6/` folder:

```text
python -m pip install pytest pytest-cov behave ruff
python -m pytest -q
python -m pytest --cov=registration --cov-report=term-missing
python -m behave
```
