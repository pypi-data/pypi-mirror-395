import re
from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup


@dataclass
class ParseSearchItem:
    title: str
    cover_url: str
    likes: str
    views: str
    href: str  # 原始href 不一定有https://


ParseSearchResult = List[ParseSearchItem]


# https://javday.tv/search/?wd=91cm-166
def parse_search(html: str) -> ParseSearchResult:
    soup = BeautifulSoup(html, "lxml")
    # htmltree = etree.fromstring(html, etree.HTMLParser())

    items = soup.find_all("a", class_="videoBox")

    result = [
        ParseSearchItem(
            title=o.find(class_="title").text.strip(),
            views=o.find(class_="views").find(class_="number").text.strip(),
            likes=o.find(class_="likes").find(class_="number").text.strip(),
            cover_url=re.search(r"^background-image: url\((.*)\);$", o.find(class_="videoBox-cover")["style"]).group(1),
            href=o["href"],
        )
        for o in items
    ]

    return result
