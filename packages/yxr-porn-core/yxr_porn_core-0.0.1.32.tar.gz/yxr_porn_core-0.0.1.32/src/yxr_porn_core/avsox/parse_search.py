from typing import List

import bs4
from bs4 import BeautifulSoup
from pydantic import BaseModel


class ParseSearchItem(BaseModel):
    title: str
    product_id: str
    cover_url: str
    date_str: str  # yyyy-mm-dd
    href: str


class ParseSearchResult(BaseModel):
    data: List[ParseSearchItem] = []
    error_message: str = ""


# https://avsox.click/cn/search/FC2-3059030
def parse_search(html: str) -> ParseSearchResult:
    soup = BeautifulSoup(html, "lxml")
    # htmltree = etree.fromstring(html, etree.HTMLParser())

    alert_div: List[bs4.Tag] = soup.find_all("div", class_="alert-danger")
    if len(alert_div) == 1:
        return ParseSearchResult(error_message=alert_div[0].find_all("h4")[0].get_text().strip())

    items = soup.find_all("div", class_="item")
    result = [
        ParseSearchItem(
            title=o.find("img")["title"],
            product_id=o.find_all("date")[0].text.strip(),
            cover_url=o.find("img")["src"],
            date_str=o.find_all("date")[1].text.strip(),
            href="https:" + o.a["href"],
        )
        for o in items
    ]

    return ParseSearchResult(data=result)
