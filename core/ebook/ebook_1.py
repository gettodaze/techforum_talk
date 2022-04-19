from __future__ import annotations

from ebooklib import epub
import typing as tp
import requests
from requests import Response
import bs4
from pathlib import Path

OUTPUT_DIR = Path("/home/mccloskey/src/john/techforum_webscraping/output")
INPUT_DIR = Path("/home/mccloskey/src/john/techforum_webscraping/input")


def main(title: str, input_path: Path) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    chapter = epub.EpubHtml(
        title=title, content=input_path.read_text(), file_name="file1.xhtml"
    )

    book = epub.EpubBook()
    book.add_item(chapter)

    # define Table Of Contents
    book.toc = ((epub.Section("Simple book"), (chapter,)),)

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
    book.spine = ["nav", chapter]

    output_path = OUTPUT_DIR / f"{title}.epub"

    epub.write_epub(output_path, book)

    return output_path


if __name__ == "__main__":
    input_path = INPUT_DIR / "ra_cryptocurrencies.txt"
    print(main(title="RA Crypto Currency Article", input_path=input_path))
