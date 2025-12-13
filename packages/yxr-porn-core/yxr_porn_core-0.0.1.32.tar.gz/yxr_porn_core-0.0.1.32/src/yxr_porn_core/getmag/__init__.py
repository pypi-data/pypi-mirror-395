# parse_getmag.py
import datetime
import logging
import re

from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel


class SearchResultItem(BaseModel):
    title: str
    subtitle: str
    size_text: str
    url: str


# ================== Helper Functions ==================


def btfa(el: Tag, *args, **kwargs) -> list[Tag]:
    """Typed bs4 find_all that returns list."""
    return el.find_all(*args, **kwargs)


# ================== Parse Functions ==================


def parse_search(html: str) -> list[SearchResultItem]:
    """
    Example html: https://getmag.net/search?q=HSODA-069
    """
    soup = BeautifulSoup(html, "lxml")

    table = btfa(soup, "table", class_="file-list")[0]
    tbody = btfa(table, "tbody")[0]
    rows = btfa(tbody, "tr")

    results = []
    if "Found 0 results" in btfa(soup, "title")[0].text:
        return []

    for row in rows:
        cols = btfa(row, "td")
        title_col = cols[0]
        size_col = cols[1]

        link = btfa(title_col, "a")[0]

        # 提取标题和副标题
        # 提取主标题：a标签下非p标签内的文本内容
        title_parts = []
        for child in link.children:
            if child.name is None and child.strip():  # 文本节点且非空
                title_parts.append(child.strip())
            elif child.name == "b":  # 包含在b标签里的文本也算
                title_parts.append(child.get_text(strip=True))
        title = " ".join(title_parts).strip()

        p_tag = btfa(link, "p", class_="sample")
        subtitle = p_tag[0].getText().strip() if p_tag else ""

        size_text = size_col.getText().strip()
        url = link.attrs["href"]

        results.append(
            SearchResultItem(
                title=title,
                subtitle=subtitle,
                size_text=size_text,
                url=url,
            )
        )

    return results


# 定义 Pydantic 模型
class FileMeta(BaseModel):
    name: str
    size_text_kb: int  # 文件大小，单位 KB


class ParsedItem(BaseModel):
    hash: str
    release_date: int  # 时间戳，单位秒
    size_text_kb: int  # 大小，单位 KB
    title: str
    file_list: list[FileMeta]


def parse_item(html: str) -> ParsedItem:
    soup: BeautifulSoup = BeautifulSoup(html, "lxml")

    # 解析磁力链接信息
    dl_info: Tag | None = soup.find("dl", class_="torrent-info")
    if dl_info is None:
        raise ValueError("Could not find torrent-info dl element")

    dt_dd_pairs: list[tuple[Tag, Tag]] = [
        (dt, dt.find_next("dd")) for dt in dl_info.find_all("dt") if dt.find_next("dd") is not None
    ]

    # 初始化默认值
    magnet_hash: str = ""
    size_text_kb: int = 0
    release_date: int = 0
    title: str = ""

    # 辅助函数：将大小字符串转换为 KB（整数）
    def parse_size_to_kb(size_str: str) -> int:
        match = re.match(r"(\d+\.?\d*)\s*(GB|TB|MB|KB)", size_str, re.IGNORECASE)
        if not match:
            return 0
        value, unit = float(match.group(1)), match.group(2).upper()
        if unit == "KB":
            return int(value)
        elif unit == "MB":
            return int(value * 1024)
        elif unit == "GB":
            return int(value * 1024 * 1024)
        elif unit == "TB":
            return int(value * 1024 * 1024 * 1024)
        return 0

    # 辅助函数：将日期字符串转换为时间戳（秒）
    def parse_date_to_timestamp(date_str: str) -> int:
        try:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
            return int(dt.timestamp())
        except ValueError:
            return 0

    # 根据 dt 内容提取对应的 dd 值
    for dt_text, dd in dt_dd_pairs:
        dt_text_str: str = dt_text.get_text().strip()
        if dt_text_str == "Hash :":
            magnet_hash = dd.get_text().strip()
        elif dt_text_str == "Size :":
            size_text_kb = parse_size_to_kb(dd.get_text().strip())
        elif dt_text_str == "Date :":
            release_date = parse_date_to_timestamp(dd.get_text().strip())
        elif dt_text_str == "Title :":
            title_text: str = dd.find("a").get_text().strip() if dd.find("a") else ""
            # 将连续的空白替换为单个空格
            title = re.sub(r"\s+", " ", title_text)

    # 解析文件列表
    file_list: list[FileMeta] = []
    try:
        file_table: Tag | None = soup.find("table", class_="file-list")
        if file_table:
            tbody: Tag | None = file_table.find("tbody")
            if tbody:
                rows: list[Tag] = tbody.find_all("tr")
                for row in rows:
                    cols: list[Tag] = row.find_all("td")
                    name: str = (
                        cols[0].find("a").get_text().strip()
                        if cols[0].find("a", class_="__cf_email__")
                        else cols[0].get_text().strip()
                    )
                    size: int = (
                        parse_size_to_kb(cols[1].get_text().strip()) if cols[1].get("class") == ["td-size"] else 0
                    )
                    file_list.append(FileMeta(name=name, size_text_kb=size))
    except Exception:
        logging.exception("忽略文件列表解析错误")

    return ParsedItem(
        hash=magnet_hash,
        release_date=release_date,
        size_text_kb=size_text_kb,
        title=title,
        file_list=file_list,
    )
