import logging
from typing import List, cast

import bs4
from bs4 import BeautifulSoup
from pydantic import BaseModel

logger = logging.getLogger("yxr_porn_core.javdb.parse_search")


def fa(soup: bs4.Tag, *args, **kwargs) -> List[bs4.Tag]:
    return cast(List[bs4.Tag], soup.find_all(*args, **kwargs))


def f(soup: bs4.Tag, *args, **kwargs) -> bs4.Tag:
    return cast(bs4.Tag, soup.find(*args, **kwargs))


class SearchResultItem(BaseModel):
    cover_url: str
    href: str
    title: str  # no product Id
    product_id: str
    # TODO score
    release_date: str  # yyyy-mm-dd
    has_magnet: bool  # 含有磁链
    has_chinese: bool  # 含有中字
    score: str  # 打分
    comments_cnt: str  # 评价人数


# https://javdb.com/search?q=stars-931
def parse_search(html: str) -> List[SearchResultItem]:
    def trasform(item: bs4.Tag) -> SearchResultItem:
        a = f(item, "a")
        href = a.attrs["href"]
        cover_url = f(f(a, "div", class_="cover"), "img").attrs["src"]
        product_id = f(f(a, class_="video-title"), "strong").text.strip()
        title = f(a, class_="video-title").text.strip().lstrip(product_id).strip()
        release_date = f(a, class_="meta").text.strip()
        score = f(a, class_="score").text.strip().split("分")[0].strip()
        comments_cnt = f(a, class_="score").text.strip().split("由")[1].split("人")[0].strip()  # 由xxx人評
        add_ons = ""
        try:
            add_ons = f(a, class_="has-addons").text.strip()
        except Exception as e:
            logger.exception(e)

        has_chinese = "中字" in add_ons
        has_magnet = "磁鏈" in add_ons

        return SearchResultItem(
            cover_url=cover_url,
            href=href,
            title=title,
            product_id=product_id,
            release_date=release_date,
            has_chinese=has_chinese,
            has_magnet=has_magnet,
            score=score,
            comments_cnt=comments_cnt,
        )

    soup = BeautifulSoup(html, "lxml")
    return [trasform(o) for o in fa(soup, class_="movie-list")[0].find_all(class_="item")]
