from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List


class SrsDatabase(ABC):
    """
    Abstract interface for SRS (Spaced Repetition System) database implementations.

    This abstract base class defines the standard interface that all SRS database
    implementations must follow. It provides a simple API for tracking learning
    progress using spaced repetition algorithms.

    Attributes:
        database_file (str): Path to the SQLite database file.

    Example:
        >>> from srsdb import FsrsDatabase
        >>> db = FsrsDatabase("learning.db")
        >>> from datetime import datetime
        >>> now = datetime.now()
        >>> db.answer(now, "question_1", correctness=85)
        >>> due = db.next(now)
        >>> print(due)
        []
    """

    def __init__(self, database_file: str) -> None:
        """
        Initialize the SRS database with a file path.

        Args:
            database_file (str): Path to the database file. The file will be created
                if it doesn't exist.

        Example:
            >>> db = FsrsDatabase("my_flashcards.db")
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

        This method updates the learning state based on how well the user answered
        a question. It automatically schedules the next review based on the
        underlying SRS algorithm.

        Args:
            now (datetime): The time that the question was answered (doesn't have to be
                the real 'now' for testing purposes).
            question_key (str): Unique identifier for the question. Can be any string
                that uniquely identifies the learning item.
            correct (int): Value from 0-100 indicating correctness:
                - 0 = completely wrong
                - 100 = completely correct
                - Values in between = degrees of correctness
                Internally converted to an appropriate value for the underlying SRS system.

        Raises:
            ValueError: If correct is not in the range 0-100.

        Example:
            >>> from datetime import datetime
            >>> db.answer(datetime.now(), "vocab_hello", 90)  # Got it mostly right
            >>> db.answer(datetime.now(), "vocab_goodbye", 40)  # Struggled with this
        """
        pass

    @abstractmethod
    def next(self, now: datetime) -> List[str]:
        """
        Returns the questions that are due as of 'now'.

        This method retrieves all questions that should be reviewed at or before
        the specified time. The ordering depends on the implementation but typically
        prioritizes cards that are most overdue or most likely to be forgotten.

        Args:
            now (datetime): The current time to check against.

        Returns:
            List[str]: List of question keys in chronological order of due date.
                Returns an empty list if no questions are due.

        Example:
            >>> from datetime import datetime, timedelta
            >>> now = datetime.now()
            >>> db.answer(now, "card_1", 50)
            >>> tomorrow = now + timedelta(days=1)
            >>> due_cards = db.next(tomorrow)
            >>> print(due_cards)
            ['card_1']
        """
        pass

    @abstractmethod
    def next_due_date(self) -> Optional[datetime]:
        """
        Returns the date/time of the next moment that a question is due.

        This is useful for scheduling notifications or knowing when the user
        should next review their cards.

        Returns:
            Optional[datetime]: The next due date, or None if no questions are scheduled.

        Example:
            >>> next_review = db.next_due_date()
            >>> if next_review:
            ...     print(f"Next review at: {next_review}")
            ... else:
            ...     print("No cards scheduled")
            Next review at: 2024-01-15 10:30:00
        """
        pass
