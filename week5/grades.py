"""Turn an exam score into a letter grade."""


def letter_grade(score):
    """Return the letter grade for a score between 0 and 100."""
    if score < 0 or score > 100:
        raise ValueError("score must be between 0 and 100")
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"
