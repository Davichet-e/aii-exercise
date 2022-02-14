import enum

import bs4
import httpx
from aii.entities.news import News
from aii.repositories.exceptions import DatabaseException
from aii.repositories.sqlite_repository import SQLiteRepository
from aii.services.exceptions import (
    InternalErrorException,
    NewsNotStoredException,
    RetrieveNewsException,
)


class Mode(enum.Enum):
    """Represent the kind of parsing that the parser will make"""

    XML = "xml"
    HTML = "html.parser"


_db_repository = SQLiteRepository()


def _retrieve_news_from_url(url: str, mode=Mode.XML) -> list[News]:
    try:
        response = httpx.get(url)
        response.raise_for_status()

    except httpx.RequestError as exception:
        raise RetrieveNewsException() from exception

    soup = bs4.BeautifulSoup(response.content, mode.value)
    return [News.from_bs4_tag(item) for item in soup.find_all("item")]


def store_news(url: str, mode=Mode.XML):
    """Retrieve news from the url and store them in the DB."""
    news = _retrieve_news_from_url(url, mode)
    try:
        _db_repository.insert_news(news)

    except DatabaseException as exception:
        raise InternalErrorException() from exception


def retrieve_news_from_db() -> list[News]:
    """Retrieve a list with the news stored in the DB
    """
    if not _db_repository.has_stored_news():
        raise NewsNotStoredException()

    try:
        return _db_repository.retrieve_stored_news()

    except DatabaseException as exception:
        raise InternalErrorException() from exception


def filter_news_by_month(month: str) -> list[News]:
    """Retrieve a list with the news stored in the DB
    """
    if not _db_repository.has_stored_news():
        raise NewsNotStoredException()

    try:
        return _db_repository.retrieve_stored_news_by_month(month)

    except DatabaseException as exception:
        raise InternalErrorException() from exception


def filter_news_by_day(day: str) -> list[News]:
    """Retrieve a list with the news stored in the DB
    """
    if not _db_repository.has_stored_news():
        raise NewsNotStoredException()

    try:
        return _db_repository.retrieve_stored_news_by_day(day)

    except DatabaseException as exception:
        raise InternalErrorException() from exception
