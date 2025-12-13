import logging
import re
from typing import List

import bs4
from bs4 import BeautifulSoup
from pydantic import BaseModel

logger = logging.getLogger("yxr_porn_core.fc2.parse_item")


def btfa(el: bs4.Tag, *args, **kwargs) -> List[bs4.Tag]:
    """bs4_typed_find_all"""
    return el.find_all(*args, **kwargs)


class ParseItemResult(BaseModel):
    product_id: str = ""
    title: str = ""
    cover_url: str = ""
    writer: str = ""
    # actresses: List[str] = []
    avg_rating: str = ""
    release_date: str = ""  # yyyy/mm/dd
    # sample_video: str = ""
    follower_cnt: int = 0
    review_cnt: int = 0
    sample_images: List[str] = []
    # length: int = 0  # mm:ss => min
    tags: List[str] = []  # タグ: str

    error_code: str = ""  # 例如 "404 Not Found"


# https://adult.contents.fc2.com/article/4400670/
def parse_item(html: str) -> ParseItemResult:
    soup = BeautifulSoup(html, "lxml")
    html_title = btfa(soup, "title")[0].getText()
    res = re.search(r"^(.*)(FC2-PPV-[0-9]+)$", html_title)
    if res is None:
        return ParseItemResult(error_code=html_title)
    product_id = re.sub("PPV-", "", res.group(2))
    hi = btfa(soup, class_="items_article_headerInfo")[0]
    ul = btfa(hi, "ul", recursive=False)[0]
    lis = btfa(ul, "li", recursive=False)

    title = res.group(1).strip()
    cover_url = "https:" + btfa(btfa(soup, class_="items_article_MainitemThumb")[0], "img")[0].attrs["src"]
    writer = btfa(lis[2], "a")[0].getText().strip()
    avg_rating = (
        btfa(
            btfa(
                btfa(btfa(soup, class_="items_article_reviewComp")[0], "section", recursive=False)[0],
                class_="items_article_Stars",
            )[0],
            "span",
            recursive=False,
        )[0]
        .getText()
        .strip()
    )
    release_date = btfa(hi, class_="items_article_Releasedate")[0].getText().strip()[-len("2024/04/21") :]
    # sample_video = btfa(soup, class_="main-video")[0].attrs["src"]
    follower_cnt = int(lis[0].getText().strip()[len("Followers") :].strip())
    review_cnt = int(lis[1].getText().strip())
    sample_images = [
        "https:" + o.attrs["href"] for o in btfa(btfa(soup, class_="items_article_SampleImagesArea")[0], "a")
    ]
    tags = [o.getText().strip() for o in btfa(btfa(soup, class_="items_article_TagArea")[0], "a")]

    return ParseItemResult(
        product_id=product_id,
        title=title,
        cover_url=cover_url,
        writer=writer,
        avg_rating=avg_rating,
        release_date=release_date,
        # sample_video=sample_video,
        follower_cnt=follower_cnt,
        review_cnt=review_cnt,
        sample_images=sample_images,
        tags=tags,
    )
