from __future__ import annotations

from ebooklib import epub
import typing as tp
import requests
from requests import Response
import bs4


class Chapter(tp.NamedTuple):
    title: str
    text: str
    num: int

    def to_epub(self) -> epub.EpubHtml:
        epub.EpubHtml(
            title=self.title,
            file_name=f"{self.num}.xhtml",
            lang="jp",
            content=self.text,
        )


def response_to_text(response: requests.Response, num: int) -> Chapter:
    bs = bs4.BeautifulSoup(response.text)
    title = str(bs.find(attrs={"class": "novel_subtitle"}))
    lines = []
    for p in bs.find_all("p"):
        id_ = p.get("id")
        if id_ and id_.startswith("L"):
            lines.append(str(p))

    return Chapter(title=title, text="\n".join(lines), num=num)


def gen_responses(novel_id: str, num_chapters: int) -> tp.Iterator[Response]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    for chapter in range(1, num_chapters + 1):
        url = f"{url_base}/{novel_id}/{chapter}"
        yield requests.get(url, cookies=cookies, headers=headers)


def get_chapters(novel_id: str, num_chapters: int) -> list[Chapter]:
    return [
        response_to_text(response, num=i)
        for i, response in enumerate(gen_responses(novel_id, num_chapters), 1)
    ]


class Book(tp.NamedTuple):
    id_: str
    title: str
    num_chapters: int

    def get_chapters(self) -> list[dict[str, str]]:
        return get_chapters(novel_id=self.id_, num_chapters=self.num_chapters)


isekai_1 = Book("test", "title", 38)

chapters = Book.get_chapters(isekai_1)


book = epub.EpubBook()

# set metadata
book.set_identifier("my_id")
book.set_title("Sample book")
book.set_language("jp")

book.add_author("Author Authorowski")
book.add_author(
    "Danko Bananko", file_as="Gospodin Danko Bananko", role="ill", uid="coauthor"
)

# create chapter
c1 = epub.EpubHtml(title="Intro", file_name="chap_01.xhtml", lang="hr")
c1.content = "<h1>Intro heading</h1><p>Zaba je skocila u baru.</p>"

# add chapter
book.add_item(c1)

# define Table Of Contents
book.toc = (
    epub.Link("chap_01.xhtml", "Introduction", "intro"),
    (epub.Section("Simple book"), (c1,)),
)

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = "BODY {color: white;}"
nav_css = epub.EpubItem(
    uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style
)

# add CSS file
book.add_item(nav_css)

# basic spine
book.spine = ["nav", c1]

# write to the file
epub.write_epub("test.epub", book, {})
