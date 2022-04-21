from __future__ import annotations

from ebooklib import epub
import typing as tp
import requests
from requests import Response
import bs4
from pathlib import Path

OUTPUT_DIR = Path("/home/mccloskey/src/john/techforum_talk/output")
INPUT_DIR = Path("/home/mccloskey/src/john/techforum_talk/input")


class Chapter(tp.NamedTuple):
    title: str
    text: str
    num: int

    def to_epub(self) -> epub.EpubHtml:
        epub.EpubHtml(
            title=self.title,
            file_name=f"{self.num}.xhtml",
            content=self.text,
        )


def html_to_chapter(html_path: Path, num: int) -> Chapter:

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


def main(title: str, input_path: Path) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    chapter = epub.EpubHtml(
        title=title, content=input_path.read_text(), file_name="file1.xhtml"
    )

    book = epub.EpubBook()
    book.add_item(chapter)

    # # define Table Of Contents
    # book.toc = ((epub.Section("Simple book"), (chapter,)),)

    # # add default NCX and Nav file
    # book.add_item(epub.EpubNcx())
    # book.add_item(epub.EpubNav())

    # # define CSS style
    # style = "BODY {color: white;}"
    # nav_css = epub.EpubItem(
    #     uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style
    # )

    # # add CSS file
    # book.add_item(nav_css)

    # basic spine
    book.spine = [chapter]

    output_path = OUTPUT_DIR / f"{title}.epub"

    epub.write_epub(output_path, book)

    return output_path


if __name__ == "__main__":
    input_path = (
        INPUT_DIR / "Cryptocurrencies The Power of Memes | Research Affiliates.html"
    )
    print(main(title="RA Crypto Currency Article HTML", input_path=input_path))
