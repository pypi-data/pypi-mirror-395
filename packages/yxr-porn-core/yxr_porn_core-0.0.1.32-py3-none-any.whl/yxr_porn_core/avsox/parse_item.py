from typing import List

from lxml import etree
from pydantic import BaseModel


class ParseItemResult(BaseModel):
    title: str
    product_id: str
    cover_url: str
    actors: List[str] = []  # 演员
    length: str  # min
    date_str: str  # yyyy-mm-dd
    studio: str = ""  # 制作商
    series: str = ""  # 系列
    genre: List[str] = []  # tags


# https://javmenu.com/zh/FC2-1851398
def parse_item(html: str) -> ParseItemResult:
    # soup = BeautifulSoup(html, "lxml")
    htmltree = etree.HTML(html, etree.HTMLParser())

    expr_number = '//span[contains(text(),"识别码:")]/../span[2]/text()'
    expr_actor = '//a[@class="avatar-box"]/span/text()'
    # expr_actorphoto = '//a[@class="avatar-box"]'
    expr_title = "/html/body/div[2]/h3/text()"
    expr_studio = '//p[contains(text(),"制作商: ")]/following-sibling::p[1]/a/text()'
    expr_release = '//span[contains(text(),"发行时间:")]/../text()'
    expr_cover = "/html/body/div[2]/div[1]/div[1]/a/img/@src"
    # expr_smallcover = '//*[@id="waterfall"]/div/a/div[1]/img/@src'
    expr_tags = '//span[@class="genre"]/a/text()'
    expr_series = '//p[contains(text(),"系列:")]/following-sibling::p[1]/a/text()'
    expr_runtime = '//span[contains(text(),"长度:")]/../text()'

    product_id = htmltree.xpath(expr_number)[0].upper()
    title = htmltree.xpath(expr_title)[0].replace("/", "_").strip(product_id).strip()
    cover_url = htmltree.xpath(expr_cover)[0]
    date_str = htmltree.xpath(expr_release)[0].strip()
    length = htmltree.xpath(expr_runtime)[0].replace("分钟", "").strip()
    studio = htmltree.xpath(expr_studio)[0].strip()
    series = htmltree.xpath(expr_series)[0].strip()

    return ParseItemResult(
        title=title,
        product_id=product_id.replace("FC2-PPV", "FC2"),
        cover_url=cover_url,
        date_str=date_str,
        length=length,
        studio=studio,
        series=series,
        genre=[s.strip() for s in htmltree.xpath(expr_tags)],
        actors=[s.strip() for s in htmltree.xpath(expr_actor)],
    )
