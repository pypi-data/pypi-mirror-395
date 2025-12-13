import logging
import re
from typing import List, cast

import bs4
from bs4 import BeautifulSoup
from pydantic import BaseModel

logger = logging.getLogger("yxr-porn-core.javdb")


def btfa(el: bs4.Tag, *args, **kwargs) -> List[bs4.Tag]:
    """bs4_typed_find_all"""
    return el.find_all(*args, **kwargs)


def btf(el: bs4.Tag, *args, **kwargs) -> bs4.Tag:
    """bs4_typed_find_all"""
    return cast(bs4.Tag, el.find(*args, **kwargs))


class AItem(BaseModel):
    text: str
    url: str


class JavDBTop250(BaseModel):
    type: str
    rank: int


class ItemStruct(BaseModel):
    title: str
    cover_url: str
    product_id: str
    lang: str  # 页面语言
    release_date: str = ""  # yyyy-mm-dd
    length: str = ""  # 时长 min
    maker: str = ""  # 片商
    seller: str = ""  # 卖家 一般fc2
    publish: str = ""  # 发行
    director: str = ""  # 导演
    series: str = ""  # 系列
    score: str = ""  # 评分
    score_users: str = ""  # 评分人数
    tags: List[AItem] = []
    actress: List[AItem] = []  # 女演员
    actors: List[AItem] = []  # 男演员
    gallery: List[str]  # 预览图
    top250: List[JavDBTop250] = []


# https://javdb.com/v/Yn1GOB
def parse_item(html: str) -> ItemStruct:
    soup = BeautifulSoup(html, "lxml")

    video_detail = btf(soup, "div", class_="video-detail")
    title_h2 = btf(video_detail, class_="title")
    product_id = btf(title_h2, "strong").text.strip()
    title = btf(title_h2, "strong", class_="current-title").text.strip()

    video_meta_panel = btf(video_detail, "div", class_="video-meta-panel")
    cover_url = btf(video_meta_panel, "img", class_="video-cover").attrs["src"]

    panel_blocks = video_meta_panel.find_all("div", class_="panel-block")
    try:
        gallery = [o["href"] for o in btf(soup, "div", class_="preview-images").find_all("a", class_="tile-item")]
    except Exception as e:
        logging.exception(e)
        gallery = []

    lang = btf(soup, "body").attrs["data-lang"]

    ret = ItemStruct(
        lang=lang,
        title=title,
        cover_url=cover_url,
        product_id=product_id,
        gallery=gallery,
    )
    for panel in panel_blocks:
        strong: bs4.Tag = panel.find("strong")
        if strong is None:  # 底部的 xxx人想看, xxx人看过
            continue
        label: str = strong.text.strip()
        value_span: bs4.Tag = panel.find("span", class_="value")
        if label in ["番號:", "ID:"]:
            ret.product_id = value_span.text.strip()
        elif label in ["日期:", "Released Date:"]:
            ret.release_date = value_span.text.strip()
        elif label in ["類別:", "Tags:"]:
            ret.tags = [AItem(text=o.text, url=o["href"]) for o in value_span.find_all("a")]
        elif label in ["演員:", "Actor(s):"]:
            a_s = value_span.find_all("a")
            strong_s = value_span.find_all("strong")
            ret.actors = []
            ret.actress = []
            # assert len(a_s) == len(strong_s)
            for i in range(len(strong_s)):
                if strong_s[i].text == r"♀":
                    ret.actress.append(AItem(text=a_s[i].text, url=a_s[i]["href"]))
                else:
                    ret.actors.append(AItem(text=a_s[i].text, url=a_s[i]["href"]))
        elif label in ["時長:", "Duration:"]:
            ret.length = value_span.text.replace("分鍾", "").replace("minute(s)", "").strip()
        elif label in ["片商:", "Maker:"]:
            ret.maker = value_span.text.strip()
        elif label in ["賣家:", "Seller:"]:
            ret.seller = value_span.text.strip()
        elif label in ["發行:", "Publisher:"]:
            ret.publish = value_span.text.strip()
        elif label in ["導演:", "Director:"]:
            ret.director = value_span.text.strip()
        elif label.startswith("系列:"):
            ret.series = value_span.text.strip()
        elif label in ["評分:", "Rating:"]:
            score_text = value_span.text.strip()
            if lang == "en":
                ret.score = score_text.split(",")[0].strip()
                ret.score_users = score_text.split("by")[1].split("user")[0].strip()
            elif lang == "zh":
                ret.score = score_text.split("分")[0].strip()
                ret.score_users = score_text.split("由")[1].split("人")[0].strip()
            else:
                logger.warning(f"unhandle lang=[{lang}] score_text=[{score_text}]")
        else:
            logger.warning(f"yxr-porn-core.javdb.parse_item unhandle label [{label}]")
    tags = btfa(soup, "a", class_="tags has-addons")
    for tag in tags:
        # 获取 No. 后面的数字
        number_span = tag.find("span", class_="tag is-dark")
        rank = int(number_span.text.replace("No.", ""))  # 去掉 "No." 前缀，保留数字

        title_span = tag.find("span", class_="tag is-warning tooltip")
        title_text = title_span.text

        match = re.search(r"JavDB\s+(.*?)\s*TOP250", title_text)
        target_text = match.group(1).strip() if match else ""
        ret.top250.append(JavDBTop250(rank=rank, type=target_text))
    return ret
