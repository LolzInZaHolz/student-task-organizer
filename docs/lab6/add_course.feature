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
