"""Characterization tests for the legacy tuition-fee code.

Every test in this file pins down what ``legacy_fees.calc`` does today, so that
the refactored ``fees`` module can be compared against it after each small step.
"""

import pytest

from fees import Course, StudentType, process_all, report, tuition_fee
from legacy_fees import calc


def legacy_courses(*hours):
    return [{"h": h} for h in hours]


def courses(*hours):
    return [Course(h) for h in hours]


def student(name, kind):
    return {"name": name, "type": kind, "courses": courses(3), "summer": False}


@pytest.mark.parametrize(
    "hours, code, kind, summer",
    [
        ((3, 3, 3), 1, StudentType.REGULAR, False),
        ((3, 3, 3, 3, 3, 3), 1, StudentType.REGULAR, True),
        ((3, 4), 2, StudentType.STAFF_CHILD, False),
        ((3, 3), 3, StudentType.SCHOLARSHIP, True),
    ],
)
def test_same_result_as_legacy(hours, code, kind, summer):
    old = calc(legacy_courses(*hours), code, 2026, summer, None)
    new = tuition_fee(courses(*hours), kind, summer)
    assert new == old


def test_large_fee_gets_reduction():
    # 18 hours x 350 = 6300 > 6000, so 200 is taken off
    assert tuition_fee(courses(6, 6, 6), StudentType.REGULAR) == 6100


def test_scholarship_student_is_not_skipped():
    students = [
        student("Sara", StudentType.REGULAR),
        student("Omar", StudentType.SCHOLARSHIP),
    ]
    assert process_all(students) == {"Sara": 1050, "Omar": 0}


def test_staff_child_pays_half_rate():
    assert tuition_fee(courses(3, 4), StudentType.STAFF_CHILD) == 1225


def test_summer_adds_a_surcharge():
    assert tuition_fee(courses(3), StudentType.REGULAR, summer=True) == 1200


def test_discount_and_extras_are_applied():
    fee = tuition_fee(courses(3), StudentType.REGULAR, discount=500, extras=(100, 50))
    assert fee == 700


def test_report_returns_text_instead_of_printing():
    assert report(courses(3), StudentType.REGULAR) == "Student fee: 1050"


def test_report_flags_a_high_fee():
    text = report(courses(6, 6, 6), StudentType.REGULAR)
    assert text == "Student fee: 6100\nHigh fee"
