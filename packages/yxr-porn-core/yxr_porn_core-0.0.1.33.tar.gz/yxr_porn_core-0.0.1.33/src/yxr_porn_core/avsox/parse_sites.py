from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup


@dataclass
class ParseSitesResult:
    sites: List[str]


# 'https://tellme.pw/avsox'
def parse_sites(html: str) -> ParseSitesResult:
    soup = BeautifulSoup(html, "lxml")
    # htmltree = etree.fromstring(html, etree.HTMLParser())

    sites = [strong.find("a")["href"] for strong in soup.find_all("strong")]

    return ParseSitesResult(sites=sites)
