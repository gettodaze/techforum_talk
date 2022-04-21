import requests

BASE_URL = "https://jisho.org/api/v1/search"


def call_api(keyword: str) -> dict:
    response = requests.get(f"{BASE_URL}/words?keyword={keyword}")
    response.raise_for_status()
    return response.json()


def main() -> None:
    keyword = input("Keyword? ")
    print(call_api(keyword))


if __name__ == "__main__":
    main()
