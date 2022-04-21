import json

import requests

BASE_URL = "https://jisho.org/api/v1/search"


def call_api(keyword: str) -> dict:
    response = requests.get(f"{BASE_URL}/words?keyword={keyword}")
    response.raise_for_status()
    return response.json()


def main() -> None:
    keyword = input("Keyword? ")
    print(json.dumps(call_api(keyword), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
