from __future__ import annotations
import json

import requests
import typing as tp

BASE_URL = "https://jisho.org/api/v1/search"
JsonT = tp.Dict[str, tp.Any]


def get_dictstring(d, start=None, end=None):
    def entry_to_text(entry):
        japanese_words = [
            f'{w.get("word") or ""} ({w.get("reading") or ""})' for w in entry["entry"]
        ]
        entry_str = "; ".join(japanese_words) + "\n"
        for n, sense in entry["senses"].items():
            semicolon = "; " if n < len(entry["senses"]) else ""
            def_str = f"({n}) " + sense + semicolon
            entry_str += def_str
        return entry_str

    if start is None or start >= len(d) or start < 0:
        start = 0
    if end is None or end > len(d) or end < 0:
        end = len(d)
    ret = ""
    keys = list(d.keys())
    for i in range(start, end):
        letter = keys[i]
        linebreak = "" if i == start else "\n\n"
        ret += linebreak + letter + ". "
        ret += entry_to_text(d[letter])

    return ret


def num_to_letter(num):
    return chr(num + 64)


def strip_senses(senses):
    ret = {}
    for i, sense in enumerate(senses):
        tdef = ", ".join(sense["english_definitions"])
        ret[i + 1] = tdef
    return ret


def strip_entry(entry):
    new_entry = {
        "senses": strip_senses(entry["senses"]),
        "entry": entry["japanese"],
    }
    return new_entry


def resp_to_dict(response_json: JsonT) -> dict[str, dict[str, str]]:
    ret = {}
    data = response_json["data"]
    for i, entry in enumerate(data):
        ret[num_to_letter(i + 1)] = strip_entry(entry)
    return ret


def call_api(keyword: str) -> JsonT:
    response = requests.get(f"{BASE_URL}/words?keyword={keyword}")
    response.raise_for_status()
    return response.json()


def main() -> None:
    keyword = input("Keyword? ")
    response_json = call_api(keyword)

    # print(json.dumps(resp_to_dict(response_json), indent=2))
    print(get_dictstring(resp_to_dict(response_json)))


if __name__ == "__main__":
    main()
