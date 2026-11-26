"""Turn an exam score into a letter grade."""

MIN_SCORE = 0
MAX_SCORE = 100

A_MIN = 90
B_MIN = 80
C_MIN = 70
D_MIN = 60

# Highest threshold first: the first threshold a score reaches is its grade.
GRADE_THRESHOLDS = (
    (A_MIN, "A"),
    (B_MIN, "B"),
    (C_MIN, "C"),
    (D_MIN, "D"),
)
FAILING_GRADE = "F"


def letter_grade(score):
    """Return the letter grade for a score between 0 and 100."""
    if score < MIN_SCORE or score > MAX_SCORE:
        raise ValueError(f"score must be between {MIN_SCORE} and {MAX_SCORE}")
    for threshold, grade in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return FAILING_GRADE
