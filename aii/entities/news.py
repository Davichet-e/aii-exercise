"""
Simple wrapper and utilities regarding news.
"""
from __future__ import annotations

import datetime
import locale
from typing import NamedTuple

import bs4


class News(NamedTuple):
    """Represent the structure of news.
    """

    title: str
    link: str
    date: datetime.datetime

    def __str__(self):
        return "\n".join([str(elem) for elem in [*self]])

    @classmethod
    def from_bs4_tag(
        cls,
        tag: bs4.Tag,
        date_format="%a, %d %b %Y %H:%M:%S %z",
        datetime_locale="en_US",
    ) -> News:
        """
        Return an instance of `News` given a `bs4.Tag`.

        params:
            - tag: The tag to parse.
            - date_format: the format of the dates to be parsed
            - datetime_locale: the locale that the dates follows
        """
        locale.setlocale(locale.LC_TIME, datetime_locale)

        title = tag.find("title").string.strip()

        link = tag.find("link").string.strip()

        date_as_string = tag.find("pubDate").string.strip()
        date = datetime.datetime.strptime(date_as_string, date_format)

        return cls(title, link, date)
