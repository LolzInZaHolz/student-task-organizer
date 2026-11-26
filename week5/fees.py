"""Tuition fees for the Student Services App.

Step 1 of the refactoring plan: ``legacy_fees.calc`` moved into its own module
with the dead code removed. Behaviour is unchanged, including the known bug in
``process_all``, which is fixed in step 7.
"""

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Course:
    """One registered course, measured in credit hours."""

    hours: int


class StudentType(Enum):
    """Why a student pays the rate they pay."""

    REGULAR = 1
    STAFF_CHILD = 2
    SCHOLARSHIP = 3


def tuition_fee(courses, kind, summer=False, discount=0, extras=[]):
    total = 0
    for c in courses:
        if kind == StudentType.REGULAR:
            total = total + c.hours * 350
        elif kind == StudentType.STAFF_CHILD:
            total = total + c.hours * 350 * 0.5
        elif kind == StudentType.SCHOLARSHIP:
            total = total + 0
    if total > 6000:
        total = total - 200
    if summer == True:
        total = total + 150
    if discount != None:
        total = total - discount
    for e in extras:
        total = total + e
    return total


def report(courses, kind, summer=False, discount=0):
    x = tuition_fee(courses, kind, summer, discount)
    if kind == StudentType.REGULAR:
        print("Student fee: " + str(x))
    elif kind == StudentType.STAFF_CHILD:
        print("Staff child fee: " + str(x))
    if x > 6000:
        print("High fee")
    return x


def process_all(students):
    for st in students:
        if st["type"] == StudentType.REGULAR:
            fee = tuition_fee(st["courses"], st["type"], st["summer"])
        if st["type"] == StudentType.STAFF_CHILD:
            fee = tuition_fee(st["courses"], st["type"], st["summer"])
        print(st["name"], fee)
