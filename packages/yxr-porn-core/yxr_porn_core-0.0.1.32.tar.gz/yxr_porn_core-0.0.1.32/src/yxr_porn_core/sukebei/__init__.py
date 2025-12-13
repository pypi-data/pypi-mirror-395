# parse_getmag.py
import re
from datetime import datetime

from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel


class SukebeiTorrentItem(BaseModel):
    title: str  # 标题
    url: str  # 详情页链接（/view/xxx）
    download_link: str  # 种子下载链接（/download/xxx.torrent）
    magnet_link: str  # 磁力链
    category: str  # 分类名称（如 "Real Life - Videos"）
    size: str  # 文件大小（如 "1.2 GiB"）
    date: datetime  # 发布时间（datetime 类型）
    seeders: int  # 做种人数
    leechers: int  # 下载人数
    downloads: int  # 完成下载次数


# ================== Helper Functions ==================


def btfa(el: Tag, *args, **kwargs) -> list[Tag]:
    """Typed bs4 find_all that returns list."""
    return el.find_all(*args, **kwargs)


# ================== Parse Functions ==================


def parse_search(html: str) -> list[SukebeiTorrentItem]:
    """
    Example html: https://sukebei.nyaa.si/?f=0&c=0_0&q=MIMK-136
    """
    soup = BeautifulSoup(html, "lxml")
    items = []

    for tr in soup.select("table.torrent-list tbody tr"):
        tds = tr.find_all("td")

        # 正确索引映射（注意 colspan="2" 的影响）
        category_td = tds[0]
        name_td = tds[1]  # colspan=2，占据两个位置
        link_td = tds[2]
        size_td = tds[3]
        date_td = tds[4]
        seeders_td = tds[5]
        leechers_td = tds[6]
        downloads_td = tds[7]

        # 提取分类名称
        category_img = category_td.find("img", class_="category-icon")
        category = category_img["alt"].strip() if category_img else "Unknown"

        # 提取标题和详情页链接
        name_a = name_td.find("a", href=lambda h: h and "/view/" in h)
        title = re.sub(r"\s+", " ", name_a.get_text()).strip() if name_a else ""
        detail_url = name_a["href"] if name_a else ""

        # 提取下载链接和磁力链
        download_link = ""
        magnet_link = ""
        for a in link_td.find_all("a", href=True):
            href = a["href"]
            if href.endswith(".torrent"):
                download_link = href
            elif href.startswith("magnet:"):
                match = re.search(r"btih:([0-9a-fA-F]{40})", href)
                if match:
                    magnet_link = match.group(1)

        # 提取文件大小
        size = size_td.get_text().strip()

        # 提取日期并转换为 datetime
        date_str = date_td.get_text().strip()
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            date = None

        # 提取做种数 / 下载数 / 完成下载次数
        seeders = int(seeders_td.get_text(strip=True))
        leechers = int(leechers_td.get_text(strip=True))
        downloads = int(downloads_td.get_text(strip=True))

        # 构建模型对象
        items.append(
            SukebeiTorrentItem(
                title=title,
                url=detail_url,
                download_link=download_link,
                magnet_link=magnet_link,
                category=category,
                size=size,
                date=date,
                seeders=seeders,
                leechers=leechers,
                downloads=downloads,
            )
        )

    return items


class SukebeiItemDetail(BaseModel):
    title: str
    category: str
    date: datetime
    submitter: str
    information: str | None = None
    seeders: int
    leechers: int
    file_size: str
    completed: int
    info_hash: str
    download_link: str
    description: str | None = None
    file_list: list[str]


def parse_item(html: str) -> SukebeiItemDetail:
    soup = BeautifulSoup(html, "lxml")
    panel_body = soup.select_one(".panel-body")
    assert panel_body is not None, "Missing .panel-body"

    # Step 1 & 2: 初始化字段 + 遍历每个 col-md-1 并提取对应值
    title = (
        re.sub(r"\s+", " ", soup.select_one(".panel-title").get_text()).strip()
        if soup.select_one(".panel-title")
        else ""
    )

    category = ""
    date = None
    submitter = ""
    information = ""
    file_size = ""
    completed = 0
    seeders = 0
    leechers = 0
    info_hash = ""

    for label in panel_body.select(".col-md-1"):
        key = label.get_text(strip=True)
        next_div = label.find_next_sibling(lambda tag: tag.name == "div" and "col-md-5" in tag.get("class", []))

        if not next_div:
            continue

        value = next_div.get_text(strip=True)

        if key == "Category:":
            links = next_div.find_all("a")
            if len(links) >= 2:
                category = f"{links[0].get_text(strip=True)} - {links[1].get_text(strip=True)}"
        elif key == "Date:":
            try:
                date = datetime.strptime(value, "%Y-%m-%d %H:%M UTC")
            except ValueError:
                pass
        elif key == "Submitter:":
            a_tag = next_div.find("a")
            if a_tag:
                submitter = a_tag.get_text().strip()
        elif key == "Information:":
            a_tag = next_div.find("a")
            if a_tag and a_tag.has_attr("href"):
                information = a_tag["href"]
        elif key == "File size:":
            file_size = value
        elif key == "Completed:":
            try:
                completed = int(value)
            except ValueError:
                pass
        elif key == "Seeders:":
            span = next_div.find("span")
            if span:
                try:
                    seeders = int(span.get_text().strip())
                except ValueError:
                    pass
        elif key == "Leechers:":
            span = next_div.find("span")
            if span:
                try:
                    leechers = int(span.get_text().strip())
                except ValueError:
                    pass
        elif key == "Info hash:":
            kbd = next_div.find("kbd")
            if kbd:
                info_hash = kbd.get_text().strip()

    # 下载链接和磁力链
    download_link = ""
    footer = soup.select_one(".panel-footer")
    if footer:
        torrent_a = footer.select_one("a[href$='.torrent']")
        if torrent_a:
            download_link = torrent_a.attrs["href"]

    # 描述
    description = ""
    desc_tag = soup.select_one("#torrent-description")
    if desc_tag:
        description = desc_tag.get_text(strip=True)

    # 文件列表
    file_list = []
    file_list_tag = soup.select_one(".torrent-file-list ul li ul")
    if file_list_tag:
        for li in file_list_tag.find_all("li"):
            name_span = li.find("i", class_="fa fa-file")
            if name_span:
                file_name = "".join(li.stripped_strings)
                file_list.append(file_name)

    return SukebeiItemDetail(
        title=title,
        category=category,
        date=date,
        submitter=submitter,
        information=information,
        seeders=seeders,
        leechers=leechers,
        file_size=file_size,
        completed=completed,
        info_hash=info_hash,
        download_link=download_link,
        description=description,
        file_list=file_list,
    )
