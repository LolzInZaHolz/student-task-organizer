"""Tuition fees for the Student Services App.

Step 2 of the refactoring plan: the remaining cryptic names are spelled out.
Behaviour is unchanged, including the known bug in ``process_all``, which is
fixed in step 7.
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
    for course in courses:
        if kind == StudentType.REGULAR:
            total = total + course.hours * 350
        elif kind == StudentType.STAFF_CHILD:
            total = total + course.hours * 350 * 0.5
        elif kind == StudentType.SCHOLARSHIP:
            total = total + 0
    if total > 6000:
        total = total - 200
    if summer == True:
        total = total + 150
    if discount != None:
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
    if fee > 6000:
        print("High fee")
    return fee


def process_all(students):
    for student in students:
        if student["type"] == StudentType.REGULAR:
            fee = tuition_fee(student["courses"], student["type"], student["summer"])
        if student["type"] == StudentType.STAFF_CHILD:
            fee = tuition_fee(student["courses"], student["type"], student["summer"])
        print(student["name"], fee)
