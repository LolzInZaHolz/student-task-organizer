# Part D - Gherkin scenarios for our team project

**Story:** N3E2-19 "Add courses" (EPIC-01, course management, 2 points).
*As a student, I want to add my courses so that I can organize my tasks by subject.*

| Scenario | Type |
| --- | --- |
| 1. Add a course with a name and a code | Happy path |
| 2. Refuse a course name that already exists | Refused / error |
| 3. Limit the length of a course name (1, 100 and 101 characters) | Edge / outline |

The expected results follow the current API in `routers/courses.py` and `models.py`.
Step definitions are not written yet, so these scenarios are not run by `behave`.
The same text is in [`add_course.feature`](add_course.feature).

```gherkin
Feature: Add a course
  As a student
  I want to add my courses
  So that I can organize my tasks by subject

  Background:
    Given the course list is empty

  Scenario: Add a course with a name and a code
    When the student adds the course "Software Engineering" with code "CS301"
    Then the course is saved
    And the course list shows "Software Engineering" with code "CS301"

  Scenario: Refuse a course name that already exists
    Given the course "Mathematics" has been added
    When the student adds the course "mathematics" with code "MTH101"
    Then the course is refused with "A course with that name already exists"
    And the course list contains 1 course

  Scenario Outline: Limit the length of a course name
    When the student adds a course whose name has <length> characters
    Then the result is "<result>"
    And the course list contains <count> courses

    Examples:
      | length | result   | count |
      | 1      | accepted | 1     |
      | 100    | accepted | 1     |
      | 101    | refused  | 0     |
```
