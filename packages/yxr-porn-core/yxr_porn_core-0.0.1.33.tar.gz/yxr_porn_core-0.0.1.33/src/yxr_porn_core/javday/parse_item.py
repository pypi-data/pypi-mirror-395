from dataclasses import dataclass
from typing import List

from lxml import etree


@dataclass
class Actor:
    name: str
    url: str


@dataclass
class ParseItemResult:
    title: str
    product_id: str
    cover_url: str
    actors: List[Actor]
    # date_str: str  # yyyy-mm-dd
    studio: str


# https://javmenu.com/zh/FC2-1851398
def parse_item(html: str) -> ParseItemResult:
    # soup = BeautifulSoup(html, "lxml")
    htmltree = etree.HTML(html, etree.HTMLParser())

    # expr_url = '/html/head/meta[@property="og:url"]/@content'
    expr_cover = '/html/head/meta[@property="og:image"]/@content'
    # expr_tags = '/html/head/meta[@name="keywords"]/@content'
    expr_title = "/html/head/title/text()"
    expr_actor = "//span[@class='vod_actor']/a/text()"
    expr_studio = '//span[@class="producer"]/a/text()'
    expr_number = '//span[@class="jpnum"]/text()'

    product_id = htmltree.xpath(expr_number)[0].upper()
    title = htmltree.xpath(expr_title)[0].replace(product_id, "").replace("- JAVDAY.TV", "").strip()
    cover_url = htmltree.xpath(expr_cover)[0]

    actors = htmltree.xpath(expr_actor)
    studio = htmltree.xpath(expr_studio)[0]

    return ParseItemResult(title=title, product_id=product_id, cover_url=cover_url, actors=actors, studio=studio)
