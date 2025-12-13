import re
from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup


@dataclass
class AItem:
    text: str
    url: str


@dataclass
class DetailItem:
    title: str
    cover_url: str
    tags: List[AItem]
    artists: List[AItem]
    product_id: str
    date_str: str
    length: str
    director: str
    producers: str
    distributor: str
    torrents: List[AItem]
    sample_images: List[str]


def re_pick(s: str, regstr: str) -> str:
    res = re.search(regstr, s)
    return "" if res is None else res.group(1).strip()


def parse_detail(html: str) -> DetailItem:
    soup = BeautifulSoup(html, "lxml")
    container = soup.find("div", class_="container")
    big_image = container.find("a", class_="bigImage").img
    cover_url = big_image["src"]
    title = big_image["title"]
    info = container.find("div", class_="info")
    info_text = info.text

    product_id = re_pick(info_text, "識別碼: (.*)")
    date_str = re_pick(info_text, "發行日期: (.*)")
    length = re_pick(info_text, "長度: (.*)分鐘")
    director = re_pick(info_text, "導演: (.*)")
    producers = re_pick(info_text, "製作商: (.*)")
    distributor = re_pick(info_text, "發行商: (.*)")

    genres = info.find_all("label")
    tags = [AItem(text=o.text, url=o.find("a")["href"]) for o in genres]
    artists = [AItem(text=o.text, url=o.a["href"]) for o in info.find_all("div", class_="star-name")]

    sample_waterfall = container.find("div", id="sample-waterfall")
    sample_images = []
    if sample_waterfall:
        sample_images = [o["href"] for o in sample_waterfall.find_all("a", class_="sample-box")]

    return DetailItem(
        title=title,
        cover_url=cover_url,
        tags=tags,
        artists=artists,
        product_id=product_id,
        date_str=date_str,
        length=length,
        director=director,
        producers=producers,
        distributor=distributor,
        torrents=[],  # TODO https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid=54156904142&lang=zh&img=/pics/cover/9nhk_b.jpg&uc=0&floor=731
        sample_images=sample_images,
    )
