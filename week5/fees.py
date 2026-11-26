"""Tuition fees for the Student Services App.

Step 3 of the refactoring plan: the magic numbers are named. Behaviour is
unchanged, including the known bug in ``process_all``, which is fixed in step 7.
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


def tuition_fee(courses, kind, summer=False, discount=0, extras=[]):
    total = 0
    for course in courses:
        if kind == StudentType.REGULAR:
            total = total + course.hours * FEE_PER_HOUR
        elif kind == StudentType.STAFF_CHILD:
            total = total + course.hours * FEE_PER_HOUR * STAFF_CHILD_RATE
        elif kind == StudentType.SCHOLARSHIP:
            total = total + course.hours * FEE_PER_HOUR * SCHOLARSHIP_RATE
    if total > HIGH_FEE_THRESHOLD:
        total = total - HIGH_FEE_REDUCTION
    if summer == True:
        total = total + SUMMER_SURCHARGE
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
