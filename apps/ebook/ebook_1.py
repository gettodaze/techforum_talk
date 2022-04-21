from __future__ import annotations

from ebooklib import epub
import typing as tp
import requests
from requests import Response
import bs4
from pathlib import Path

OUTPUT_DIR = Path("/home/mccloskey/src/john/techforum_talk/output")
INPUT_DIR = Path("/home/mccloskey/src/john/techforum_talk/input")


def main(title: str, input_path: Path) -> Path:
    # make chapter
    chapter = epub.EpubHtml(
        title=title, content=input_path.read_text(), file_name="file1.xhtml"
    )

    # make book
    book = epub.EpubBook()
    book.add_item(chapter)
    book.spine = [chapter]

    # write book
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"{title}.epub"
    epub.write_epub(output_path, book)

    return output_path


if __name__ == "__main__":
    input_path = INPUT_DIR / "ra_cryptocurrencies.txt"
    print(main(title="RA Crypto Currency Article", input_path=input_path))
