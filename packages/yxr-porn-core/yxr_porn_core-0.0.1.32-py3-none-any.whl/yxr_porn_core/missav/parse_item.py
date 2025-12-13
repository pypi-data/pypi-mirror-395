import json
import re
from typing import cast

import bs4
from bs4 import BeautifulSoup
from pydantic import BaseModel

desc_placeholder = "免費高清日本 AV 在線看，無需下載，高速播放沒有延遲，超過十萬部影片，每日更新，開始播放後不會再有廣告，支援任何裝置包括手機，電腦及智能電視。可以番號，女優或作品系列名稱作影片搜尋。免費加入會員後可任意收藏影片供日後觀賞。"


def fa(soup: bs4.Tag, *args, **kwargs) -> list[bs4.Tag]:
    return cast(list[bs4.Tag], soup.find_all(*args, **kwargs))


def f(soup: bs4.Tag, *args, **kwargs) -> bs4.Tag:
    return cast(bs4.Tag, soup.find(*args, **kwargs))


def extract_seek_info(html: str) -> tuple[str, int]:
    """
    从 HTML 中提取 prefix url, max index

    Args:
        html (str): 包含 urls: [...] 的 HTML 字符串

    Returns:
        tuple: (prefix: str, max_index: int )
    """
    # 匹配 urls: [...] 且包含 "seek" 的数组（假设在一行）
    match = re.search(r"urls: (\[.*seek.*\]),", html)

    if not match:
        return "", 0

    json_str = match.group(1)

    try:
        urls = json.loads(json_str)  # ✅ 原生支持 \/，无需 replace
    except json.JSONDecodeError:
        return "", 0

    if not urls:
        return "", 0

    # 提取 prefix：域名后、/seek/ 前的第一个路径段
    first_url = urls[0]
    last_url = urls[-1]

    # 提取完整前缀: https://.../.../seek/
    prefix_match = re.search(r"(https?://.*/seek/)", first_url)
    prefix_url = prefix_match.group(1) if prefix_match else ""

    # 提取最大下标
    idx_match = re.search(r"_([0-9]+)\.jpg$", last_url)
    max_index = int(idx_match.group(1)) if idx_match else 0

    return prefix_url, max_index


class SearchResultItem(BaseModel):
    product_id: str = ""
    title: str = ""
    actress: list[str] = []
    release_date: str = ""  # YYYY-MM-DD maybe empty, 注意 这个日期 是meta里的 可能和 页面展示的有1天之差!?
    description: str = ""
    duration: str = ""
    url: str = ""
    cover_url: str = ""
    category: list[str] = []
    publisher: str = ""
    director: str = ""
    tags: list[str] = []
    seek_prefix: str = ""  # 时间轴预览图, 后面加上 _0.jpg一直到 _99.jpg 就是所有时间轴预览图
    seek_max_index: int = -1  # 时间轴预览图, 后面加上 _0.jpg一直到 _99.jpg 就是所有时间轴预览图


# https://missav.com/sone-315
# https://missav.com/dm24/sone-315
def parse_item(html: str) -> SearchResultItem:
    """解析 HTML 内容并返回搜索结果项。

    注意:
        该函数目前仅支持解析 missav 网站的繁体中文（zh-Hant）页面。
        不保证对其他语言版本或网站结构变更后的兼容性。

    Args:
        html (str): 来自 missav 繁体网页的 HTML 字符串。

    Returns:
        SearchResultItem: 解析后的搜索结果项对象。

    """
    soup = BeautifulSoup(html, "lxml")

    r = SearchResultItem()

    r.url = f(soup, "meta", property="og:url").attrs["content"]
    r.product_id = r.url.split("/")[-1].upper()
    r.cover_url = f(soup, "meta", property="og:image").attrs["content"]
    r.release_date = f(soup, "meta", property="og:video:release_date").attrs["content"]
    r.description = f(soup, "meta", property="og:description").attrs["content"]
    if r.description == desc_placeholder:
        r.description = ""
    r.duration = f(soup, "meta", property="og:video:duration").attrs["content"]
    r.title = f(soup, "meta", property="og:title").attrs["content"].replace(r.product_id, "").strip()
    r.actress = [meta.attrs["content"] for meta in fa(soup, "meta", property="og:video:actor")]

    info_div = f(soup, "div", class_="space-y-2")
    catespan = f(info_div, "span", string="類型:")
    r.category = [a.text for a in fa(cast(bs4.Tag, catespan.parent), "a")] if catespan else []
    publisherspan = f(info_div, "span", string="發行商:")
    r.publisher = f(cast(bs4.Tag, publisherspan.parent), "a").text if publisherspan else ""
    directorspan = f(info_div, "span", string="導演:")
    r.director = f(cast(bs4.Tag, directorspan.parent), "a").text if directorspan else ""
    labelspan = f(info_div, "span", string="標籤:")
    r.tags = [a.text for a in fa(cast(bs4.Tag, labelspan.parent), "a")] if labelspan else []

    seek_prefix, seek_maxindex = extract_seek_info(html)
    if seek_maxindex != -1:
        r.seek_prefix = seek_prefix
        r.seek_max_index = seek_maxindex

    return r
