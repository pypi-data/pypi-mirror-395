import re
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel


class ParseSearchError(Exception):
    def __init__(self, error_message: str, error_string: str, *args: object) -> None:
        super().__init__(error_message, *args)
        self.error_string = error_string
        self.error_message = error_message


class FileMeta(BaseModel):
    name: str
    size_text: str


class ParsedItem(BaseModel):
    title: str
    magnet: str
    release_date: str  # yyyy-mm-dd
    size_text: str
    file_list: list[FileMeta]


def btfa(el: Tag, *args, **kwargs) -> list[Tag]:
    """bs4_typed_find_all"""
    return el.find_all(*args, **kwargs)


# https://cilisousuo.com/magnet/ilrS
def parse_item(html: str) -> ParsedItem:
    soup = BeautifulSoup(html, "lxml")

    meta: Tag = btfa(soup, "dl", class_="meta")[0]
    title = re.sub(r"\s+", " ", btfa(soup, "h1", class_="title")[0].text.strip() or "")
    dt_s = btfa(meta, "dt")
    dd_s = btfa(meta, "dd")
    if dt_s[0].getText() != "种子特征码 :":
        msg = "Except '种子特征码 :'"
        raise ValueError(msg)
    magnet = dd_s[0].getText()
    if dt_s[1].getText() != "发布日期 :":
        msg = "Except '发布日期 :'"
        raise ValueError(msg)
    release_date = dd_s[1].getText()
    if dt_s[2].getText() != "文件大小 :":
        msg = "Except '文件大小 :'"
        raise ValueError(msg)

    size_text = dd_s[2].getText()

    file_trs = btfa(btfa(btfa(soup, "table", class_="files")[0], "tbody")[0], "tr")

    return ParsedItem(
        title=title,
        magnet=magnet,
        release_date=release_date,
        size_text=size_text,
        file_list=[
            FileMeta(name=btfa(f, "td")[0].getText(), size_text=btfa(f, class_="td-size")[0].getText())
            for f in file_trs
        ],
    )
