from dataclasses import dataclass
from typing import List

import bs4
from bs4 import BeautifulSoup


class ParseSearchError(Exception):
    def __init__(self, error_message: str, error_string: str, *args: object) -> None:
        super().__init__(error_message, *args)
        self.error_string = error_string
        self.error_message = error_message


@dataclass
class SearchResultItem:
    title: str
    subtitle: str
    size_text: str
    url: str


def btfa(el: bs4.Tag, *args, **kwargs) -> List[bs4.Tag]:
    """bs4_typed_find_all"""
    return el.find_all(*args, **kwargs)


# https://cilisousuo.com/search?q=FSDSS-761
def parse_search(html: str) -> List[SearchResultItem]:
    soup = BeautifulSoup(html, "lxml")

    ul: bs4.Tag = btfa(soup, "ul", class_="list")[0]
    items: List[bs4.Tag] = btfa(ul, "li", class_="item")

    return [
        SearchResultItem(
            title=btfa(item, class_="result-title")[0].getText().strip(),
            subtitle=btfa(item, class_="filename")[0].getText().strip(),
            size_text=btfa(item, class_="size")[0].getText().strip(),
            url=btfa(item, class_="link")[0].attrs["href"],
        )
        for item in items
    ]
