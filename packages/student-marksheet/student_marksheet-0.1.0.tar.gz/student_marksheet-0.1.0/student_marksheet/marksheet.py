from __future__ import annotations
import logging
from typing import Dict, Union

# Configure library-level logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())  # Prevent unwanted default logging

class Marksheet:
    """
    A simple class to manage and calculate a student's marksheet.

    Features:
        - Add subject-wise marks
        - Calculate total marks, percentage, and grade
        - Export in JSON/dict or formatted text form

    Example (doctest):
        >>> m = Marksheet("Swami", 1)
        >>> m.add_mark("Math", 90)
        >>> m.add_mark("Science", 80)
        >>> m.total()
        170
        >>> round(m.percentage(), 2)
        85.0
        >>> m.grade()
        'A'
    """

    def __init__(self, student_name: str, roll_no: Union[int, str]) -> None:
        """
        Initialize a new marksheet for a student.

        Args:
            student_name: Name of the student.
            roll_no: Roll number or unique ID.

        Example:
            >>> m = Marksheet("John", 5)
            >>> m.student_name
            'John'
            >>> m.roll_no
            5
        """
        self.student_name: str = student_name
        self.roll_no: Union[int, str] = roll_no
        self.marks: Dict[str, float] = {}

        logger.debug(f"Created Marksheet for {student_name} (Roll {roll_no})")

    def add_mark(self, subject: str, score: Union[int, float]) -> None:
        """
        Add or update a subject mark.

        Args:
            subject: Name of the subject.
            score: Score between 0 and 100.

        Raises:
            ValueError: If score is not numeric or outside valid range.

        Example:
            >>> m = Marksheet("Swami", 1)
            >>> m.add_mark("Math", 95)
            >>> m.marks["Math"]
            95
        """
        if not isinstance(score, (int, float)):
            raise ValueError("Score must be a number.")
        if not (0 <= score <= 100):
            raise ValueError("Score must be between 0 and 100.")

        self.marks[subject] = float(score)
        logger.info(f"Added score: {score} for subject '{subject}'")

    def total(self) -> float:
        """
        Returns the total marks.

        Example:
            >>> m = Marksheet("Swami", 1)
            >>> m.add_mark("Math", 50)
            >>> m.add_mark("Sci", 25)
            >>> m.total()
            75
        """
        total_value = sum(self.marks.values())
        logger.debug(f"Computed total: {total_value}")
        return total_value

    def percentage(self) -> float:
        """
        Calculates the percentage.

        Returns:
            A float value between 0 and 100.

        Example:
            >>> m = Marksheet("Swami", 1)
            >>> m.add_mark("Math", 60)
            >>> m.add_mark("Sci", 40)
            >>> m.percentage()
            50.0
        """
        if len(self.marks) == 0:
            return 0.0

        percentage_value = self.total() / len(self.marks)
        logger.debug(f"Computed percentage: {percentage_value}")
        return percentage_value

    def grade(self) -> str:
        """
        Determines the grade from percentage.

        Grade Rules:
            A+ : >= 90
            A  : >= 75
            B  : >= 60
            C  : >= 45
            D  : < 45

        Example:
            >>> m = Marksheet("Swami", 1)
            >>> m.add_mark("Math", 100)
            >>> m.add_mark("Sci", 80)
            >>> m.grade()
            'A'
        """
        p = self.percentage()
        logger.debug(f"Evaluating grade for percentage: {p}")

        if p >= 90:
            return "A+"
        elif p >= 75:
            return "A"
        elif p >= 60:
            return "B"
        elif p >= 45:
            return "C"
        else:
            return "D"

    def export_json(self) -> Dict[str, Union[str, int, float, dict]]:
        """
        Export the marksheet as a JSON/dict.

        Example:
            >>> m = Marksheet("Swami", 1)
            >>> m.add_mark("Math", 90)
            >>> data = m.export_json()
            >>> data["grade"]
            'A+'
        """
        data = {
            "student_name": self.student_name,
            "roll_no": self.roll_no,
            "marks": self.marks,
            "total": self.total(),
            "percentage": self.percentage(),
            "grade": self.grade()
        }
        logger.debug(f"Exported JSON data: {data}")
        return data

    def export_text(self) -> str:
        """
        Export the marksheet as formatted text.

        Example:
            >>> m = Marksheet("Swami", 1)
            >>> m.add_mark("Math", 100)
            >>> "Math" in m.export_text()
            True
        """
        text = f"Marksheet for {self.student_name} (Roll {self.roll_no})\n"
        text += "--------------------------------------------------\n"

        for subject, score in self.marks.items():
            text += f"{subject}: {score}\n"

        text += "--------------------------------------------------\n"
        text += f"Total: {self.total()}\n"
        text += f"Percentage: {self.percentage():.2f}%\n"
        text += f"Grade: {self.grade()}\n"

        logger.debug("Exported text format marksheet.")
        return text
