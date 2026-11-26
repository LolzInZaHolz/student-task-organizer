"""Tuition fees for the Student Services App.

Step 5 of the refactoring plan: the mutable default becomes an immutable tuple
and the remaining truthiness comparisons are cleaned up. Behaviour is unchanged,
including the known bug in ``process_all``, which is fixed in step 7.
"""

from dataclasses import dataclass
from enum import Enum

FEE_PER_HOUR = 350
STAFF_CHILD_RATE = 0.5
SCHOLARSHIP_RATE = 0.0

HIGH_FEE_THRESHOLD = 6000
HIGH_FEE_REDUCTION = 200
SUMMER_SURCHARGE = 150


@dataclass(frozen=True)
class Course:
    """One registered course, measured in credit hours."""

    hours: int


class StudentType(Enum):
    """Why a student pays the rate they pay."""

    REGULAR = 1
    STAFF_CHILD = 2
    SCHOLARSHIP = 3


# One row per student type: adding a type means adding a row, not editing a chain.
RATES = {
    StudentType.REGULAR: FEE_PER_HOUR,
    StudentType.STAFF_CHILD: FEE_PER_HOUR * STAFF_CHILD_RATE,
    StudentType.SCHOLARSHIP: FEE_PER_HOUR * SCHOLARSHIP_RATE,
}


def tuition_fee(courses, kind, summer=False, discount=0, extras=()):
    total = sum(RATES[kind] * course.hours for course in courses)
    if total > HIGH_FEE_THRESHOLD:
        total = total - HIGH_FEE_REDUCTION
    if summer:
        total = total + SUMMER_SURCHARGE
    total = total - discount
    for extra in extras:
        total = total + extra
    return total


def report(courses, kind, summer=False, discount=0):
    fee = tuition_fee(courses, kind, summer, discount)
    if kind == StudentType.REGULAR:
        print("Student fee: " + str(fee))
    elif kind == StudentType.STAFF_CHILD:
        print("Staff child fee: " + str(fee))
    if fee > HIGH_FEE_THRESHOLD:
        print("High fee")
    return fee


def process_all(students):
    for student in students:
        if student["type"] == StudentType.REGULAR:
            fee = tuition_fee(student["courses"], student["type"], student["summer"])
        if student["type"] == StudentType.STAFF_CHILD:
            fee = tuition_fee(student["courses"], student["type"], student["summer"])
        print(student["name"], fee)
