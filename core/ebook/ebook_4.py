from __future__ import annotations
import uuid

from ebooklib import epub
import typing as tp
import requests
from requests import Response
import bs4
from pathlib import Path

OUTPUT_DIR = Path("/home/mccloskey/src/john/techforum_talk/output")
INPUT_DIR = Path("/home/mccloskey/src/john/techforum_talk/input")


def html_to_chapter(html_path: Path) -> epub.EpubHtml:
    soup = bs4.BeautifulSoup(html_path.read_text(), features="html.parser")
    [title_box] = soup.findAll(**{"class": "hero__box"})
    [title_element] = title_box.findAll(**{"class": "hero__title"})
    title = title_element.text
    [publication_keypoints] = soup.findAll(**{"class": "publication__keypoints"})
    [publication_body] = soup.findAll(**{"class": "publication__body"})
    fname = f"{uuid.uuid4()}.xhtml"
    content = f"{title_box}{publication_keypoints}{publication_body}"
    return epub.EpubHtml(title=title, content=content, file_name=fname)


def main(input_paths: tp.Iterable[Path], title: str) -> Path:
    # make chapter
    chapters = [html_to_chapter(path) for path in input_paths]

    # make book
    book = epub.EpubBook()
    book.spine = ["nav"] + chapters
    for c in chapters:
        book.add_item(c)
    book.toc = ((epub.Section(title), chapters),)
    # add default Nav file
    book.add_item(epub.EpubNav())

    # write book
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"{title}.epub"
    epub.write_epub(output_path, book)

    return output_path


if __name__ == "__main__":
    input_paths = [
        INPUT_DIR / fn
        for fn in (
            "Cryptocurrencies The Power of Memes | Research Affiliates.html",
            "ESG Is a Preference, Not a Strategy | Research Affiliates.html",
        )
    ]
    print(main(input_paths=input_paths, title="RA Publication Chapters"))
