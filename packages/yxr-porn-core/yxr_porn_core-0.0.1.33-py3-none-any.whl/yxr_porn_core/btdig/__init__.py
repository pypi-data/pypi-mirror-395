from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel


class FileItem(BaseModel):
    name: str
    size: str | None = None  # 可能为空（如目录）


class SearchResultItem(BaseModel):
    title: str
    url: str
    files_count: int
    total_size: str
    age: str
    file_list: list[FileItem]


# ================== Helper Functions ==================


def btfa(el: Tag, *args, **kwargs) -> list[Tag]:
    """Typed bs4 find_all that returns list."""
    return el.find_all(*args, **kwargs)


# ================== Parse Functions ==================


def parse_search(html: str) -> list[SearchResultItem]:
    """
    Example html: https://en.btdig.com/search?q=MIMK-136
    """
    soup = BeautifulSoup(html, "lxml")

    results = []

    result_items = soup.find_all("div", class_="one_result")
    if not result_items:
        return results

    for item in result_items:
        # 标题和链接
        name_div = item.find("div", class_="torrent_name")
        a_tag = name_div.find("a") if name_div else None
        title = a_tag.get_text().strip() if a_tag else ""
        url = a_tag["href"] if a_tag and "href" in a_tag.attrs else ""

        # 文件数量
        files_count_span = item.find("span", class_="torrent_files")
        files_count = int(files_count_span.text.strip()) if files_count_span else 0

        # 总大小
        total_size_span = item.find("span", class_="torrent_size")
        total_size = total_size_span.text.strip() if total_size_span else ""

        # 时间
        age_span = item.find("span", class_="torrent_age")
        age = age_span.text.strip() if age_span else ""

        # 文件列表解析
        excerpt_div = item.find("div", class_="torrent_excerpt")
        file_list = []

        if excerpt_div:
            for div in btfa(excerpt_div, "div"):
                fa_class = div.get("class", [])
                if "fa-file" in " ".join(fa_class):  # 是文件项
                    name = div.get_text().strip() or ""
                    size_span = div.find_next("span")
                    size = size_span.text.strip() if size_span else ""
                    if name:
                        file_list.append(FileItem(name=name, size=size))

        results.append(
            SearchResultItem(
                title=title,
                url=url,
                files_count=files_count,
                total_size=total_size,
                age=age,
                file_list=file_list,
            )
        )

    return results


class TorrentInfo(BaseModel):
    name: str
    size: str
    age: str
    files: int


def parse_item(html_content: str) -> TorrentInfo:
    soup = BeautifulSoup(html_content, "lxml")  # 使用 lxml 引擎解析

    name = soup.find("td", string="Name:").find_next_sibling("td").get_text().strip()
    size = soup.find("td", string="Size:").find_next_sibling("td").get_text().strip()
    age = soup.find("td", string="Age:").find_next_sibling("td").get_text().strip()
    files = int(soup.find("td", string="Files:").find_next_sibling("td").get_text().strip())

    return TorrentInfo(name=name, size=size, age=age, files=files)
