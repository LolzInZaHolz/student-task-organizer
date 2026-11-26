# Week 5 — Static analysis findings

Scope: `week5/legacy_fees.py`, copied unchanged from the handout (the tuition-fee
code "inherited" from a previous team). Nothing in that file was edited, so the
measurements in `before.txt` stay reproducible.

Tools: Ruff 0.17.6 and Pylint 4.1.4 on Python 3.14.7. Raw terminal output is in
[`before.txt`](before.txt); the after-numbers are in [`after.md`](after.md).

## 1. Findings table

Ruff reports **17 problems** in the file. Every rule is mapped to the lecture
smell and to the refactoring that removes it.

| Rule | Count | Smell (lecture name) | Refactoring |
| --- | --- | --- | --- |
| F401 | 2 | Dead code — unused imports (`os`, `math`) | Delete the imports |
| PLR2004 | 6 | Magic numbers (`1`, `2`, `3`, `6000`, `6000`, `2`) | Replace with named constants / an enum |
| C901 | 1 | Long, complex function — the `if/elif` chain over the type code | Replace the chain with a rate table (`RATES`) |
| PLR0913 | 1 | Long parameter list — six parameters, four of them one-letter names | Delete the unused argument, group the rest |
| PLR0917 | 1 | Too many positional arguments | Same fix as PLR0913 |
| ARG001 | 1 | Unused parameter `y` (the year, never read) | Delete it, and the `2026` at every call site |
| B006 | 1 | Mutable default argument `extra=[]` shared across calls | Use an immutable tuple default |
| E711 | 1 | Comparison to `None` with `!=` | Use `is not None` (then remove it: the default is `0`) |
| E712 | 1 | Comparison to `True` with `==` | Use truthiness: `if summer:` |
| F841 | 1 | Dead code — unused variable `tmp` | Delete the assignment |
| N802 | 1 | Function name `ProcessAll` is not `snake_case` | Rename to `process_all` |

### Why 17 and not the 16 in the handout

The handout's summary lists 16 problems. Our run finds one more, **PLR0917
(`too-many-positional-arguments`)**, which is reported alongside PLR0913 for the
same `calc(d, t, y, s, disc, extra=[])` signature. PLR0917 was added to Ruff
after the handout was written, so the handout's count reflects an older Ruff.
The smell and the fix are the same; only the rule bookkeeping differs.

## 2. Smells the tools did not report

Ruff and Pylint find patterns, not meaning. These five problems need a human
reader, and each one was removed in the refactoring:

| # | Smell | Where | Why it hurts |
| --- | --- | --- | --- |
| 1 | Mysterious names | `d`, `t`, `y`, `s`, `disc`, `x`, `st`, `c`, `h` | `N` rules only police letter case. A reader cannot tell that `d` is a list of courses or that `s` means "summer". |
| 2 | Duplicated call / shotgun surgery | `ProcessAll` calls `calc(...)` twice with the same arguments except the literal type | Adding a student type means editing this loop too. The type is already in `st["type"]`, so the branch is redundant. |
| 3 | Mixed responsibilities | `report` calculates **and** prints; `ProcessAll` calculates **and** prints | The fee can only be obtained by running something that writes to stdout, so it cannot be reused or tested cleanly. |
| 4 | Primitive obsession | `{"h": 3}` dictionaries and the integer type codes `1/2/3` | Nothing stops a typo such as `{"hours": 3}`; the meaning of `2` lives only in a comment. |
| 5 | Duplicated knowledge | `350` appears in all three branches of the chain | The hourly rate is a business rule repeated three times, so a rate change is a three-place edit (a DRY / OCP violation). |

A sixth, smaller one: `elif t == 3: total = total + 0` is a **no-op branch**. It
looks like scholarships are handled, but the branch only adds zero — which is
exactly why the bug in `ProcessAll` went unnoticed.

## 3. The hidden bug in `ProcessAll`

```python
from legacy_fees import ProcessAll

ProcessAll([
    {"name": "Sara", "type": 1, "courses": [{"h": 3}], "summer": False},
    {"name": "Omar", "type": 3, "courses": [{"h": 3}], "summer": False},
])
# Sara 1050
# Omar 1050
```

`fee` is a single local variable that is only assigned inside the `type == 1`
and `type == 2` branches. For a scholarship student (`type == 3`) **neither**
branch runs, so `fee` still holds the value from the previous loop iteration and
Omar is printed with Sara's 1050 instead of 0. Put the scholarship student first
and the same code raises `UnboundLocalError: cannot access local variable 'fee'`
— the output of the handout is only "correct-looking" because a paying student
happens to run first.

Pylint flags this as `E0606 possibly-used-before-assignment`; Ruff does not see
it at all, which is the clearest example in this lab of a linter warning being
about *how* the code is written while the bug is about *what* it does.

## 4. Pylint second opinion

```
Your code has been rated at 4.86/10
```

Pylint's own names for the same problems: `unused-import`, `unused-argument`,
`unused-variable`, `dangerous-default-value`, `singleton-comparison`,
`invalid-name`, `too-many-arguments`. It adds checks Ruff did not run here:
missing module/function docstrings, and the `possibly-used-before-assignment`
that points straight at the bug above.
