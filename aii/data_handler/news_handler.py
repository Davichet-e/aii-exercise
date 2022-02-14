import enum
import httpx
from aii.data_access.db import DBHandler
from aii.data_access.exceptions import DatabaseException
from aii.data_handler.exceptions import RetrieveNewsException
from aii.entities.news import News
import bs4


class Mode(enum.Enum):
    XML = "xml"
    HTML = "html.parser"


_db_handler = DBHandler()


def retrieve_news(url: str, mode: Mode = Mode.XML) -> list[News]:
    """Retrieve a list with the news of the url.
    """
    if _db_handler.has_stored_news():
        try:
            return _db_handler.retrieve_stored_news()
        except DatabaseException as exception:
            raise RetrieveNewsException(
                "Internal error retrieving the stored news"
            ) from exception

    response = httpx.get(url)

    if response.status_code != httpx.codes.OK:
        raise RetrieveNewsException("Error retrieving the news from the url.")

    soup = bs4.BeautifulSoup(response.content, mode.value)

    return [News.from_bs4_tag(item) for item in soup.find_all("item")]
