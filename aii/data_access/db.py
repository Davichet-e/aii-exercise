from datetime import datetime
import sqlite3
from aii.data_access.exceptions import DatabaseException

from aii.entities.news import News


class DBHandler:
    _con = sqlite3.connect(":memory:")
    _cur = _con.cursor()

    def __init__(self) -> None:
        # FIXME: Change to sqlite_master when not using in-memory db
        if not self.has_stored_news():
            self._create_news_table()

    @staticmethod
    def destroy():
        DBHandler._con.close()

    def has_stored_news(self):
        self._cur.execute(
            """ SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='news' """
        )

        return self._cur.fetchone()[0] == 1

    def _create_news_table(self):
        self._cur.execute(
            """
        CREATE TABLE news(
            news_id INTEGER PRIMARY KEY NOT NULL,
            title VARCHAR(100) NOT NULL,
            link VARCHAR(50) NOT NULL,
            publication_date VARCHAR(50) NOT NULL
        )
        """
        )

    def retrieve_stored_news(self) -> list[News]:
        try:

            return [
                News(
                    title,
                    link,
                    datetime.strptime(publication_date, "%Y-%m-%d %H:%M:%S"),
                )
                for title, link, publication_date in self._cur.execute(
                    """SELECT * FROM news"""
                )
            ]
        except sqlite3.OperationalError as e:
            raise DatabaseException("An error related to the database ocurred.") from e

    def insert_news(self, news: list[News]) -> None:
        try:
            self._cur.executemany("INSERT INTO news VALUES (?)", news)
        except sqlite3.OperationalError as e:
            raise DatabaseException("An error related to the database ocurred.") from e
