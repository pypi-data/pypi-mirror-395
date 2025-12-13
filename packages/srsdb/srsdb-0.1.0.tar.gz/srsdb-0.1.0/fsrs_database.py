import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple
from srs_database import SrsDatabase


class FsrsDatabase(SrsDatabase):
    """
    Implementation of SrsDatabase using the FSRS (Free Spaced Repetition Scheduler) algorithm.

    FSRS uses a sophisticated algorithm that tracks difficulty, stability, and retrievability
    of cards to optimize review scheduling.
    """

    def __init__(self, database_file: str):
        """
        Initialize the FSRS database with a file path.

        Args:
            database_file: Path to the SQLite database file
        """
        super().__init__(database_file)
        self._conn: Optional[sqlite3.Connection] = None
        self._is_open = False

    def _open(self) -> None:
        """
        Opens or creates the database and ensures the FSRS-specific schema exists.

        The schema includes:
        - cards table: stores card state (stability, difficulty, last review, etc.)
        - reviews table: stores review history
        """
        if self._is_open:
            return

        self._conn = sqlite3.connect(self.database_file)
        self._conn.row_factory = sqlite3.Row

        cursor = self._conn.cursor()

        # Create cards table for FSRS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fsrs_cards (
                question_key TEXT PRIMARY KEY,
                difficulty REAL NOT NULL DEFAULT 0.0,
                stability REAL NOT NULL DEFAULT 0.0,
                retrievability REAL NOT NULL DEFAULT 1.0,
                state INTEGER NOT NULL DEFAULT 0,
                last_review TEXT,
                due_date TEXT NOT NULL,
                elapsed_days INTEGER NOT NULL DEFAULT 0,
                scheduled_days INTEGER NOT NULL DEFAULT 0,
                reps INTEGER NOT NULL DEFAULT 0,
                lapses INTEGER NOT NULL DEFAULT 0
            )
        """)

        # Create reviews table for tracking review history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fsrs_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_key TEXT NOT NULL,
                review_time TEXT NOT NULL,
                rating INTEGER NOT NULL,
                state INTEGER NOT NULL,
                FOREIGN KEY (question_key) REFERENCES fsrs_cards(question_key)
            )
        """)

        self._conn.commit()
        self._is_open = True

    def _close(self) -> None:
        """Close the database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
            self._is_open = False

    def _convert_correctness_to_rating(self, correct: int) -> int:
        """
        Convert correctness percentage (0-100) to FSRS rating (1-4).

        FSRS uses ratings:
        1 = Again (failed)
        2 = Hard
        3 = Good
        4 = Easy

        Args:
            correct: Correctness percentage from 0-100

        Returns:
            FSRS rating from 1-4
        """
        if correct < 25:
            return 1  # Again
        elif correct < 50:
            return 2  # Hard
        elif correct < 85:
            return 3  # Good
        else:
            return 4  # Easy

    def _calculate_next_interval(self, difficulty: float, stability: float,
                                 rating: int, state: int) -> Tuple[float, float, int, int]:
        """
        Calculate next review parameters using simplified FSRS algorithm.

        Args:
            difficulty: Current difficulty (0-10)
            stability: Current stability in days
            rating: Review rating (1-4)
            state: Current card state (0=new, 1=learning, 2=review, 3=relearning)

        Returns:
            Tuple of (new_difficulty, new_stability, new_state, scheduled_days)
        """
        # Simplified FSRS parameters
        w = [0.4, 0.6, 2.4, 5.8, 4.93, 0.94, 0.86, 0.01, 1.49, 0.14, 0.94, 2.18, 0.05, 0.34, 1.26, 0.29, 2.61]

        # Update difficulty
        new_difficulty = difficulty
        if state != 0:  # Not new
            new_difficulty = difficulty - w[6] * (rating - 3)
            new_difficulty = max(1, min(10, new_difficulty))
        else:
            new_difficulty = w[4] - (rating - 3) * w[5]
            new_difficulty = max(1, min(10, new_difficulty))

        # Calculate new stability based on rating
        if state == 0:  # New card
            if rating == 1:
                new_stability = w[0]
                new_state = 3  # Relearning
            elif rating == 2:
                new_stability = w[1]
                new_state = 1  # Learning
            elif rating == 3:
                new_stability = w[2]
                new_state = 2  # Review
            else:  # rating == 4
                new_stability = w[3]
                new_state = 2  # Review
        elif rating == 1:  # Failed review
            new_stability = w[11] * (difficulty ** -w[12]) * ((stability + 1) ** w[13]) - 1
            new_stability = max(0.1, new_stability)
            new_state = 3  # Relearning
        else:  # Successful review
            if rating == 2:
                factor = w[14]
            elif rating == 3:
                factor = w[15]
            else:  # rating == 4
                factor = w[16]

            new_stability = stability * factor
            new_state = 2  # Review

        # Calculate scheduled days (rounded)
        scheduled_days = max(1, int(round(new_stability)))

        return new_difficulty, new_stability, new_state, scheduled_days

    def answer(self, now: datetime, question_key: str, correct: int) -> None:
        """
        Records the result of the user answering a question using FSRS algorithm.

        Args:
            now: The time that the question was answered
            question_key: Unique identifier for the question
            correct: Value from 0-100 indicating correctness
        """
        self._open()

        if not 0 <= correct <= 100:
            raise ValueError(f"correct must be between 0 and 100, got {correct}")

        rating = self._convert_correctness_to_rating(correct)
        cursor = self._conn.cursor()

        # Get existing card or create new one
        cursor.execute("""
            SELECT difficulty, stability, state, last_review, reps, lapses
            FROM fsrs_cards
            WHERE question_key = ?
        """, (question_key,))

        row = cursor.fetchone()

        if row:
            difficulty = row['difficulty']
            stability = row['stability']
            state = row['state']
            last_review = datetime.fromisoformat(row['last_review']) if row['last_review'] else None
            reps = row['reps']
            lapses = row['lapses']

            # Calculate elapsed days
            elapsed_days = (now - last_review).days if last_review else 0
        else:
            # New card
            difficulty = 0.0
            stability = 0.0
            state = 0
            elapsed_days = 0
            reps = 0
            lapses = 0

        # Calculate new parameters
        new_difficulty, new_stability, new_state, scheduled_days = \
            self._calculate_next_interval(difficulty, stability, rating, state)

        # Update counters
        new_reps = reps + 1
        new_lapses = lapses + (1 if rating == 1 else 0)

        # Calculate due date
        due_date = now
        from datetime import timedelta
        due_date = now + timedelta(days=scheduled_days)

        # Update or insert card
        cursor.execute("""
            INSERT OR REPLACE INTO fsrs_cards (
                question_key, difficulty, stability, retrievability, state,
                last_review, due_date, elapsed_days, scheduled_days, reps, lapses
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            question_key, new_difficulty, new_stability, 1.0, new_state,
            now.isoformat(), due_date.isoformat(), elapsed_days, scheduled_days,
            new_reps, new_lapses
        ))

        # Record review
        cursor.execute("""
            INSERT INTO fsrs_reviews (question_key, review_time, rating, state)
            VALUES (?, ?, ?, ?)
        """, (question_key, now.isoformat(), rating, new_state))

        self._conn.commit()

    def next(self, now: datetime) -> List[str]:
        """
        Returns the questions that are due as of 'now', ordered by due date.

        Args:
            now: The current time to check against

        Returns:
            List of question keys in chronological order of due date
        """
        self._open()

        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT question_key
            FROM fsrs_cards
            WHERE due_date <= ?
            ORDER BY due_date ASC
        """, (now.isoformat(),))

        return [row['question_key'] for row in cursor.fetchall()]

    def next_due_date(self) -> Optional[datetime]:
        """
        Returns the date/time of the next moment that a question is due.

        Returns:
            The next due date, or None if no questions are scheduled
        """
        self._open()

        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT MIN(due_date) as next_due
            FROM fsrs_cards
        """)

        row = cursor.fetchone()
        if row and row['next_due']:
            return datetime.fromisoformat(row['next_due'])
        return None

    def __del__(self):
        """Cleanup: close database connection when object is destroyed."""
        self._close()
