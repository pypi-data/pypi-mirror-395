from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List


class SrsDatabase(ABC):
    """
    Abstract interface for SRS (Spaced Repetition System) database implementations.
    """

    def __init__(self, database_file: str):
        """
        Initialize the SRS database with a file path.

        Args:
            database_file: Path to the database file
        """
        self.database_file = database_file

    @abstractmethod
    def _open(self) -> None:
        """
        Opens or creates the database. If the database exists but doesn't have
        the required tables, creates those tables. Is tolerant of unrelated tables
        that might be in the database. The schema of the tables is particular to
        the underlying SRS library.

        This is a private method called internally by public methods.
        """
        pass

    @abstractmethod
    def answer(self, now: datetime, question_key: str, correct: int) -> None:
        """
        Records the result of the user answering a question.

        Args:
            now: The time that the question was answered (doesn't have to be
                 the real 'now' for testing purposes)
            question_key: Unique identifier for the question
            correct: Value from 0-100 indicating correctness. 0 means completely
                    wrong, 100 means completely correct. Everything in between is
                    a degree of correctness. Internally converted to an appropriate
                    value for the underlying SRS system.
        """
        pass

    @abstractmethod
    def next(self, now: datetime) -> List[str]:
        """
        Returns the questions that are due as of 'now'.

        Args:
            now: The current time to check against

        Returns:
            List of question keys in chronological order of due date
        """
        pass

    @abstractmethod
    def next_due_date(self) -> Optional[datetime]:
        """
        Returns the date/time of the next moment that a question is due.

        Returns:
            The next due date, or None if no questions are scheduled
        """
        pass
