from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup


@dataclass
class ListItem:
    title: str
    cover_url: str
    tags: List[str]
    product_id: str
    date_str: str
    href: str


def parse_list(html: str) -> List[ListItem]:
    soup = BeautifulSoup(html, "lxml")
    items = soup.find_all("a", class_="movie-box")
    res = []
    for a in items:
        href = a["href"]
        photo_frame = a.find(class_="photo-frame").find("img")
        cover_url = photo_frame["src"]
        title = photo_frame["title"]
        tags = [o.text for o in a.find_all("button")]
        dates = a.find_all("date")
        product_id = dates[0].text
        date_str = dates[1].text
        res.append(
            ListItem(title=title, cover_url=cover_url, tags=tags, product_id=product_id, date_str=date_str, href=href)
        )
    return res
