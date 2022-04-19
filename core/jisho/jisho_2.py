from __future__ import annotations
import json

import requests
import typing as tp

BASE_URL = "https://jisho.org/api/v1/search"
JsonT = tp.Dict[str, tp.Any]
SenseT = tp.Dict[str, tp.List[str]]


def num_to_letter(num: int) -> str:
    return chr(num + 64)


def get_english_definitions(senses: tp.Iterable[SenseT]) -> tp.Dict[int, str]:
    eng_definitions = {}
    for i, sense in enumerate(senses, 1):
        eng_definitions[i] = ", ".join(sense["english_definitions"])
    return eng_definitions


def parse_entry(entry: JsonT) -> JsonT:
    new_entry = {
        "definitions": get_english_definitions(entry["senses"]),
        "entry": entry["japanese"],
    }
    return new_entry


def parse_response(response_json: JsonT) -> JsonT:
    data = response_json["data"]
    parsed_response = {}
    for i, entry in enumerate(data, 1):
        parsed_response[num_to_letter(i)] = parse_entry(entry)
    return parsed_response


def call_api(keyword: str) -> JsonT:
    response = requests.get(f"{BASE_URL}/words?keyword={keyword}")
    response.raise_for_status()
    return response.json()


def main() -> None:
    keyword = input("Keyword? ")
    response_json = call_api(keyword)

    print(json.dumps(parse_response(response_json), indent=2))


if __name__ == "__main__":
    main()
