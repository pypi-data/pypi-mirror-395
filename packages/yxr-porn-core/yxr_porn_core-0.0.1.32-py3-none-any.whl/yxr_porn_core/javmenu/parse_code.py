import logging
from typing import List, cast

# from bs4 import BeautifulSoup
from lxml import etree
from pydantic import BaseModel

# HTMLTREE_TYPE = Any
HTMLTREE_TYPE = etree.ElementBase
logger = logging.getLogger("yxr_porn_core.javmenu.parse_code")


def typed_xpath(htmltree: HTMLTREE_TYPE, expr: str) -> List[str]:
    return cast(List[str], htmltree.xpath(expr))


class StructPeople(BaseModel):
    name: str
    url: str


class ParseCodeResult(BaseModel):
    lang: str = ""
    title: str = ""
    product_id: str = ""
    cover_url: str = ""
    length: str = ""  # min
    date_str: str = ""  # yyyy-mm-dd
    tags: List[str] = []
    publisher: str = ""
    director: str = ""
    series: str = ""
    maker: str = ""
    actresses: List[StructPeople] = []  # 女
    actors: List[StructPeople] = []  # 男
    gallery: List[str] = []  # 样图
    error_message: str = ""


def get_0_or_empty_str(htmltree: HTMLTREE_TYPE, expr: str) -> str:
    arr = typed_xpath(htmltree, expr)

    if len(arr) == 1:
        return arr[0]
    elif len(arr) == 0:
        return ""
    else:
        logger.warn("multiple director [arr_director]")
        return arr[0]


# https://javmenu.com/zh/FC2-1851398
def parse_code(html: str) -> ParseCodeResult:
    # BeautifulSoup(html, "lxml")
    htmltree: HTMLTREE_TYPE = etree.HTML(html, etree.HTMLParser())
    # TODO 判断html lang 是 ja 还是 zh
    lang = htmltree.xpath("/html")[0].attrib["lang"]

    expr_title = '/html/head/meta[@property="og:title"]/@content'
    expr_cover = '/html/head/meta[@property="og:image"]/@content'
    expr_cover2 = "(//video)[1]/@data-poster"
    expr_publisher = '//div[contains(@class,"publisher")]/a/span/text()'
    expr_director = '//div[contains(@class,"director")]/a/span/text()'
    expr_maker = '//div[contains(@class,"maker")]/a/span/text()'
    expr_series = '//div[contains(@class,"series")]//a/span/text()'
    expr_number = 'string(//div[contains(@class,"code")])'
    expr_actress = '//a[@class="actress"]'
    expr_actor = '//a[contains(@class,"actress") and contains(@class,"text-primary")]'
    expr_tags = '//a[contains(@class,"genre")]/text()'

    title = typed_xpath(htmltree, expr_title)[0]
    if title in ["JAV目录大全", "JAVカタログブック"]:  # http 302 回首页
        return ParseCodeResult(lang=lang, error_message="not found")

    cover_url = typed_xpath(htmltree, expr_cover)[0]
    if cover_url == "":
        cover_url = typed_xpath(htmltree, expr_cover2)[0]
    tags = [s.strip() for s in typed_xpath(htmltree, expr_tags)]

    # might empty
    maker = get_0_or_empty_str(htmltree, expr_maker)
    publisher = get_0_or_empty_str(htmltree, expr_publisher)
    series = get_0_or_empty_str(htmltree, expr_series)
    director = get_0_or_empty_str(htmltree, expr_director)

    actress_el = cast(List[HTMLTREE_TYPE], htmltree.xpath(expr_actress)) or []
    actor_el = cast(List[HTMLTREE_TYPE], htmltree.xpath(expr_actor)) or []

    def parse_zh() -> ParseCodeResult:
        nonlocal title
        expr_runtime = '//span[contains(text(),"时长")]/../span[2]/text()'
        expr_release = '//span[contains(text(),"日期")]/../span[2]/text()'
        expr_gallery = '//h2[contains(text(),"图片预览")]/../div/a'
        # expr_studio = '//span[contains(text(),"製作")]/../span[2]/a/text()'

        # TODO unsafe parse
        product_id: str = ("".join(htmltree.xpath(expr_number).split())).replace("番号:", "").strip().upper()

        # TODO safe parse
        title = title.replace(product_id, "")
        title = title.replace("| 每日更新", "")
        title = title.replace("| JAV目录大全", "")
        title = title.replace("免费在线看", "")
        title = title.replace("免费AV在线看", "").strip()

        date_str = typed_xpath(htmltree, expr_release)[0]
        length = typed_xpath(htmltree, expr_runtime)[0].replace("分钟", "").strip()

        gallery_el = cast(List[HTMLTREE_TYPE], htmltree.xpath(expr_gallery)) or []

        return ParseCodeResult(
            lang=lang,
            title=title,
            product_id=product_id,
            cover_url=cover_url,
            date_str=date_str,
            length=length,
            tags=tags,
            publisher=publisher,
            director=director,
            series=series,
            maker=maker,
            actresses=[StructPeople(name=o.text, url=o.attrib["href"]) for o in actress_el],
            actors=[StructPeople(name=o.text, url=o.attrib["href"]) for o in actor_el],
            gallery=[o.attrib["href"] for o in gallery_el],
        )

    def parse_ja() -> ParseCodeResult:
        nonlocal title
        expr_runtime = '//span[contains(text(),"収録時間:")]/../span[2]/text()'
        expr_release = '//span[contains(text(),"発売日:") or contains(text(),"公開日時:")]/../span[2]/text()'
        expr_gallery = '//h2[contains(text(),"画像プレビュー")]/../div/a'
        # expr_studio = '//span[contains(text(),"製作")]/../span[2]/a/text()'

        # TODO unsafe parse
        product_id: str = ("".join(htmltree.xpath(expr_number).split())).replace("品番:", "").strip().upper()

        # TODO safe parse
        title = title.replace(product_id, "")
        # title = title.replace("| 每日更新", "")
        title = title.replace("| JAVカタログブック", "")
        title = title.replace("無料で見る", "").strip()
        # title = title.replace("免费AV在线看", "").strip()

        date_str = typed_xpath(htmltree, expr_release)[0]
        length = typed_xpath(htmltree, expr_runtime)[0].replace("分", "").strip()

        # might empty
        gallery_el = cast(List[HTMLTREE_TYPE], htmltree.xpath(expr_gallery)) or []

        return ParseCodeResult(
            lang=lang,
            title=title,
            product_id=product_id,
            cover_url=cover_url,
            date_str=date_str,
            length=length,
            tags=tags,
            publisher=publisher,
            director=director,
            series=series,
            maker=maker,
            actresses=[StructPeople(name=o.text, url=o.attrib["href"]) for o in actress_el],
            actors=[StructPeople(name=o.text, url=o.attrib["href"]) for o in actor_el],
            gallery=[o.attrib["href"] for o in gallery_el],
        )

    if lang == "zh":
        return parse_zh()
    elif lang == "ja":
        return parse_ja()
    else:
        return ParseCodeResult(lang=lang, error_message=f"Unhandle lang=[{lang}]")
