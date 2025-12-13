# based on https://github.com/yoshiko2/Movie_Data_Capture/blob/master/scrapinglib/msin.py


from dataclasses import dataclass
from typing import List, cast

from lxml import etree


class ParseSearchError(Exception):
    def __init__(self, error_message: str, error_string: str, *args: object) -> None:
        super().__init__(error_message, *args)
        self.error_string = error_string
        self.error_message = error_message


@dataclass
class SearchResultItem:
    product_id: str
    title: str
    writer: str
    maker: str
    actor: List[str]
    genre: List[str]
    duration: str
    create_date: str  # YYYY-MM-DD
    release_date: str  # YYYY-MM-DD maybe empty
    cover_url: str
    label: str  # 正规厂 的 厂牌
    series: str
    category: str
    type: str


def typed_xpath(htmltree, expr: str) -> List[str]:
    return cast(List[str], htmltree.xpath(expr))


def pick0_or_empty_str(a: List[str]) -> str:
    return "" if len(a) == 0 else a[0]


# https://db.msin.jp/search/movie?str=fc2-ppv-3393451
# https://db.msin.jp/branch/search?sort=jp.movie&str=SONE-218
# cookie = {'age':'off'}
def parse_search(html: str) -> SearchResultItem:
    htmltree = etree.HTML(html, etree.HTMLParser())

    expr_err_string = '//div[@class="error_string"]/text()'
    expr_err_message = '//div[@class="error_massage"]/text()'  # 网站拼的就是 massage
    expr_category = '//div[@class="mv_category"]/text()'
    expr_type = '//div[@class="mv_type"]/text()'
    expr_createdate = '//a[@class="mv_createDate"]/text()'
    expr_releasedate = '//a[@class="mv_releaseDate"]/text()'
    expr_filename = '//div[@class="mv_fileName"]/text()'
    expr_pn = '//div[@class="mv_pn"]/text()'
    expr_title = '//div[contains(@class,"mv_title")]/text()'
    expr_duration = '//div[@class="mv_duration"]/text()'
    expr_writer = '//a[@class="mv_writer"]/text()'
    expr_actor = '//div[contains(text(),"出演者：")]/following-sibling::div[1]/div/div[@class="performer_text"]/a/text()'
    expr_maker = '//a[@class="mv_mfr"]/text()'
    expr_cover_url = '//div[@class="movie_top"]/img/@src'
    expr_label = '//a[@class="mv_label"]/text()'
    expr_series = '//a[@class="mv_series"]/text()'
    expr_genre = '//div[@class="mv_genre"]/label/text()'

    err_strings = typed_xpath(htmltree, expr_err_string)
    if len(err_strings) > 0:
        raise ParseSearchError(error_string=err_strings[0], error_message=typed_xpath(htmltree, expr_err_message)[0])

    # FC2-PPV-XYZ -> FC2-XYZ
    product_id = (
        pick0_or_empty_str(typed_xpath(htmltree, expr_pn))  # FC2 没有这个, 正规厂有这个
        or typed_xpath(htmltree, expr_filename)[0].upper().replace("FC2-PPV", "FC2").strip()
    )
    title: str = typed_xpath(htmltree, expr_title)[0].upper().replace("FC2-PPV", "FC2").replace(product_id, "").strip()
    writer: str = pick0_or_empty_str(typed_xpath(htmltree, expr_writer))
    maker: str = typed_xpath(htmltree, expr_maker)[0]
    actor: List[str] = [act.replace("（FC2動画）", "") for act in typed_xpath(htmltree, expr_actor)]
    genre: List[str] = [act.strip() for act in typed_xpath(htmltree, expr_genre)]
    duration: str = typed_xpath(htmltree, expr_duration)[0]
    release_date: str = pick0_or_empty_str(typed_xpath(htmltree, expr_releasedate))
    create_date: str = pick0_or_empty_str(typed_xpath(htmltree, expr_createdate))
    cover_url: str = typed_xpath(htmltree, expr_cover_url)[0]
    label: str = pick0_or_empty_str(typed_xpath(htmltree, expr_label))
    series: str = pick0_or_empty_str(typed_xpath(htmltree, expr_series))
    category: str = pick0_or_empty_str(typed_xpath(htmltree, expr_category))
    type_: str = pick0_or_empty_str(typed_xpath(htmltree, expr_type))

    return SearchResultItem(
        product_id=product_id,
        title=title,
        writer=writer,
        maker=maker,
        actor=actor,
        duration=duration,
        create_date=create_date,
        release_date=release_date,
        cover_url=cover_url,
        label=label,
        genre=genre,
        series=series,
        category=category,
        type=type_,
    )
