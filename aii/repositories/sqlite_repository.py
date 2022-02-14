import abc
import sqlite3
from datetime import datetime

from aii.entities.news import News
from aii.repositories.exceptions import DatabaseException


class NewsRepository(abc.ABC):
    @abc.abstractmethod
    def has_stored_news(self) -> bool:
        ...

    @abc.abstractmethod
    def retrieve_stored_news(self) -> list[News]:
        ...

    @abc.abstractmethod
    def insert_news(self, news: list[News]) -> None:
        ...


class SQLiteRepository(NewsRepository):
    _con = sqlite3.connect(":memory:")
    _cur = _con.cursor()
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"

    def __init__(self) -> None:
        # FIXME: Change to sqlite_master when not using in-memory db
        if not self._is_table_created():
            self._create_news_table()

    def has_stored_news(self) -> bool:
        if not self._is_table_created():
            return False

        self._cur.execute("""SELECT COUNT(*) FROM news""")

        return self._cur.fetchone()[0] > 0

    def _is_table_created(self) -> bool:
        self._cur.execute(
            """ SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='news' """
        )

        return self._cur.fetchone()[0] == 1

    def _create_news_table(self):
        self._cur.execute("""DROP TABLE IF EXISTS news""")
        self._cur.execute(
            """
        CREATE TABLE news(
            news_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                    datetime.strptime(publication_date, self.DATETIME_FORMAT),
                )
                for _, title, link, publication_date in self._cur.execute(
                    """SELECT * FROM news"""
                )
            ]
        except sqlite3.OperationalError as exception:
            raise DatabaseException(
                "An error related to the database ocurred."
            ) from exception

    def retrieve_stored_news_by_month(self, month: str):
        try:

            return [
                News(
                    title,
                    link,
                    datetime.strptime(publication_date, self.DATETIME_FORMAT),
                )
                for _, title, link, publication_date in self._cur.execute(
                    """SELECT * FROM news WHERE strftime('%m', publication_date) = ?""",
                    (datetime.strftime(datetime.strptime(month, "%b"), "%m"),),
                )
            ]
        except sqlite3.OperationalError as exception:
            raise DatabaseException(
                "An error related to the database ocurred."
            ) from exception

    def retrieve_stored_news_by_day(self, day: str):
        try:
            return [
                News(
                    title,
                    link,
                    datetime.strptime(publication_date, self.DATETIME_FORMAT),
                )
                for _, title, link, publication_date in self._cur.execute(
                    """SELECT * FROM news WHERE strftime('%d/%m/%Y', publication_date) = ?""",
                    (day,),
                )
            ]
        except sqlite3.OperationalError as exception:
            raise DatabaseException(
                "An error related to the database ocurred."
            ) from exception

    def insert_news(self, news: list[News]) -> None:
        try:
            self._cur.executemany(
                "INSERT INTO news (title, link, publication_date) VALUES (?, ?, ?)",
                news,
            )
        except sqlite3.OperationalError as exception:
            raise DatabaseException(
                "An error related to the database ocurred."
            ) from exception
