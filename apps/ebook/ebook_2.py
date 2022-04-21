from __future__ import annotations

from ebooklib import epub
from pathlib import Path

OUTPUT_DIR = Path("output")
INPUT_DIR = Path("input")


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
    input_path = (
        INPUT_DIR / "Cryptocurrencies The Power of Memes | Research Affiliates.html"
    )
    print(main(title="RA Crypto Currency Article HTML", input_path=input_path))
