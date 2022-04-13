from __future__ import annotations

import typing as tp

import requests
import bs4
import re
import json

BASE_BBC_URL = "https://www.bbc.com"
BBC_URL = f"{BASE_BBC_URL}/news/world/us_and_canada"


class Article(tp.NamedTuple):
    title: str
    link: str
    summary: str
    time: str
    image: str


def get_articles() -> bs4.element.ResultSet:
    response = requests.get(BBC_URL)
    soup = bs4.BeautifulSoup(response.text, features="html.parser")
    return soup.findAll("article")


def parse_article(article: bs4.element.Tag) -> Article:
    regex = re.compile("^title_.*")
    [title_element] = article.findAll(id=regex)
    text_elements = article.findAll("p")
    time_elements = article.findAll("time")
    image_elements = article.findAll("img")
    return Article(
        title=title_element.text,
        link=f'{BASE_BBC_URL}{title_element.parent.get("href")}',
        summary="; ".join([e.text for e in text_elements]),
        time="; ".join([e.text for e in time_elements]),
        image="; ".join([e.get("src") for e in image_elements]),
    )


def main():
    articles = [parse_article(a) for a in get_articles()]
    print(
        json.dumps({article.title: article._asdict() for article in articles}, indent=4)
    )
    # fmt: off
    from IPython import embed; embed() # JTODO: remove
    # fmt: on


if __name__ == "__main__":
    main()
