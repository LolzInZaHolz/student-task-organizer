"""Tuition fees for the Student Services App.

Step 7 of the refactoring plan: the hidden bug is fixed, so every student gets
a fee - including scholarship students, who used to inherit the previous
student's fee.
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
    """Return the tuition fee for one student's courses."""
    total = sum(RATES[kind] * course.hours for course in courses)
    if total > HIGH_FEE_THRESHOLD:
        total = total - HIGH_FEE_REDUCTION
    if summer:
        total = total + SUMMER_SURCHARGE
    total = total - discount
    for extra in extras:
        total = total + extra
    return total


# One label per student type, for the same reason as RATES.
REPORT_LABELS = {
    StudentType.REGULAR: "Student fee",
    StudentType.STAFF_CHILD: "Staff child fee",
    StudentType.SCHOLARSHIP: "Scholarship fee",
}


def report(courses, kind, summer=False, discount=0):
    """Return the invoice text for one student; printing is the caller's job."""
    fee = tuition_fee(courses, kind, summer, discount)
    lines = [f"{REPORT_LABELS[kind]}: {fee}"]
    if fee > HIGH_FEE_THRESHOLD:
        lines.append("High fee")
    return "\n".join(lines)


def process_all(students):
    """Return the fee for every student, keyed by name."""
    fees = {}
    for student in students:
        kind = StudentType(student["type"])
        fees[student["name"]] = tuition_fee(
            student["courses"], kind, student.get("summer", False)
        )
    return fees
