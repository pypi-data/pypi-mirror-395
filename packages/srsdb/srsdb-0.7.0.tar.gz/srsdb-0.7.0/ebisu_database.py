import sqlite3
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from srs_database import SrsDatabase

try:
    import ebisu
    EBISU_AVAILABLE = True
except ImportError:
    EBISU_AVAILABLE = False


class EbisuDatabase(SrsDatabase):
    """
    Implementation of SrsDatabase using the Ebisu Bayesian spaced repetition algorithm.

    Ebisu uses Bayesian statistics with Beta distributions and exponential forgetting
    curves to intelligently schedule reviews. It tracks a probability distribution
    on the half-life of each fact.

    Note: Requires the 'ebisu' package to be installed: pip install ebisu
    """

    def __init__(self, database_file: str):
        """
        Initialize the Ebisu database with a file path.

        Args:
            database_file: Path to the SQLite database file

        Raises:
            ImportError: If the ebisu package is not installed
        """
        if not EBISU_AVAILABLE:
            raise ImportError(
                "The 'ebisu' package is required for EbisuDatabase. "
                "Install it with: pip install ebisu"
            )

        super().__init__(database_file)
        self._conn: Optional[sqlite3.Connection] = None
        self._is_open = False

    def _open(self) -> None:
        """
        Opens or creates the database and ensures the Ebisu-specific schema exists.

        The schema includes:
        - ebisu_cards table: stores card state (alpha, beta, t, last_review, etc.)
        - ebisu_reviews table: stores review history
        """
        if self._is_open:
            return

        self._conn = sqlite3.connect(self.database_file)
        self._conn.row_factory = sqlite3.Row

        cursor = self._conn.cursor()

        # Create cards table for Ebisu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ebisu_cards (
                question_key TEXT PRIMARY KEY,
                alpha REAL NOT NULL,
                beta REAL NOT NULL,
                t REAL NOT NULL,
                last_review TEXT,
                total_reviews INTEGER NOT NULL DEFAULT 0
            )
        """)

        # Create reviews table for tracking review history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ebisu_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_key TEXT NOT NULL,
                review_time TEXT NOT NULL,
                correctness INTEGER NOT NULL,
                recall_probability REAL,
                FOREIGN KEY (question_key) REFERENCES ebisu_cards(question_key)
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

    def _convert_correctness_to_success(self, correct: int) -> float:
        """
        Convert correctness percentage (0-100) to success value (0.0-1.0).

        Ebisu supports soft-binary quizzes where success can be a float between 0 and 1.

        Args:
            correct: Correctness percentage from 0-100

        Returns:
            Success value from 0.0 to 1.0
        """
        return correct / 100.0

    def _get_time_since_review(self, now: datetime, last_review: Optional[datetime]) -> float:
        """
        Calculate time elapsed since last review in hours.

        Args:
            now: Current time
            last_review: Time of last review, or None for new cards

        Returns:
            Time elapsed in hours
        """
        if last_review is None:
            # For new cards, use a small epsilon to avoid division by zero
            return 0.1

        delta = now - last_review
        hours = delta.total_seconds() / 3600.0
        return max(0.1, hours)  # Ensure at least 0.1 hours

    def _calculate_due_date(self, model: Tuple[float, float, float],
                           now: datetime, target_recall: float = 0.5) -> datetime:
        """
        Calculate when a card should next be reviewed.

        Args:
            model: Ebisu model tuple (alpha, beta, t)
            now: Current time
            target_recall: Target recall probability (default 0.5)

        Returns:
            The datetime when the card should be reviewed
        """
        # The 't' in the model represents the half-life in hours
        # We schedule the next review at the half-life point
        alpha, beta, t = model
        hours_until_review = t

        return now + timedelta(hours=hours_until_review)

    def answer(self, now: datetime, question_key: str, correct: int) -> None:
        """
        Records the result of the user answering a question using Ebisu algorithm.

        Args:
            now: The time that the question was answered
            question_key: Unique identifier for the question
            correct: Value from 0-100 indicating correctness
        """
        self._open()

        if not 0 <= correct <= 100:
            raise ValueError(f"correct must be between 0 and 100, got {correct}")

        success = self._convert_correctness_to_success(correct)
        cursor = self._conn.cursor()

        # Get existing card or create new one
        cursor.execute("""
            SELECT alpha, beta, t, last_review, total_reviews
            FROM ebisu_cards
            WHERE question_key = ?
        """, (question_key,))

        row = cursor.fetchone()

        if row:
            # Existing card
            prior = (row['alpha'], row['beta'], row['t'])
            last_review = datetime.fromisoformat(row['last_review']) if row['last_review'] else None
            total_reviews = row['total_reviews']

            # Calculate time elapsed since last review
            tnow = self._get_time_since_review(now, last_review)

            # Calculate current recall probability before update
            recall_prob = ebisu.predictRecall(prior, tnow, exact=True)
        else:
            # New card - use default model with 24-hour initial half-life
            prior = ebisu.defaultModel(24.0)  # 24 hours
            tnow = 0.1  # Small initial time
            total_reviews = 0
            recall_prob = 1.0

        # Update the model based on the quiz result
        # Ebisu's updateRecall expects (success, total) where total is the number of quiz attempts
        # For a single quiz, total is 1, and success is between 0 and 1
        posterior = ebisu.updateRecall(prior, success, 1, tnow)

        # Update counters
        new_total_reviews = total_reviews + 1

        # Store updated card
        alpha, beta, t = posterior
        cursor.execute("""
            INSERT OR REPLACE INTO ebisu_cards (
                question_key, alpha, beta, t, last_review, total_reviews
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (question_key, alpha, beta, t, now.isoformat(), new_total_reviews))

        # Record review
        cursor.execute("""
            INSERT INTO ebisu_reviews (question_key, review_time, correctness, recall_probability)
            VALUES (?, ?, ?, ?)
        """, (question_key, now.isoformat(), correct, recall_prob))

        self._conn.commit()

    def next(self, now: datetime) -> List[str]:
        """
        Returns the questions that are due as of 'now', ordered by recall probability.

        Args:
            now: The current time to check against

        Returns:
            List of question keys ordered by recall probability (lowest first)
        """
        self._open()

        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT question_key, alpha, beta, t, last_review
            FROM ebisu_cards
        """)

        due_cards = []

        for row in cursor.fetchall():
            question_key = row['question_key']
            model = (row['alpha'], row['beta'], row['t'])
            last_review = datetime.fromisoformat(row['last_review']) if row['last_review'] else None

            # Calculate time since review
            tnow = self._get_time_since_review(now, last_review)

            # Calculate current recall probability
            recall_prob = ebisu.predictRecall(model, tnow, exact=True)

            # Consider cards "due" if recall probability is below 0.5
            if recall_prob < 0.5:
                due_cards.append((question_key, recall_prob))

        # Sort by recall probability (lowest first - most forgotten cards)
        due_cards.sort(key=lambda x: x[1])

        return [card[0] for card in due_cards]

    def next_due_date(self) -> Optional[datetime]:
        """
        Returns the date/time of the next moment that a question is due.

        For Ebisu, this is the earliest time when any card's recall probability
        drops below 0.5.

        Returns:
            The next due date, or None if no questions are scheduled
        """
        self._open()

        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT question_key, alpha, beta, t, last_review
            FROM ebisu_cards
        """)

        rows = cursor.fetchall()
        if not rows:
            return None

        earliest_due = None

        for row in rows:
            model = (row['alpha'], row['beta'], row['t'])
            last_review_str = row['last_review']

            if not last_review_str:
                # New card, due now
                return datetime.now()

            last_review = datetime.fromisoformat(last_review_str)

            # Calculate when recall probability will drop to 0.5
            # At time t (half-life), recall is approximately 0.5
            alpha, beta, t = model
            due_time = last_review + timedelta(hours=t)

            if earliest_due is None or due_time < earliest_due:
                earliest_due = due_time

        return earliest_due

    def __del__(self):
        """Cleanup: close database connection when object is destroyed."""
        self._close()
