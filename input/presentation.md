# My Title
- John McCloskey
# Intro
Hi everyone, and welcome to my talk. I'm John McCloskey and I am on a mission to get all of you to consider using python in your everyday lives. For the non-programmers out there, I know you might think, but I don't know programming, and besides where would I ever have the opportunity to use python in my every day life? I have two answers to that.
1) It's simpler than you might expect!
2) Let us go through some examples of where you might want to use python.
## Preface
- Throughout this talk, we'll be using some new packages. Just a note that if you're using the RA Platform, please create a new environment before installing any extra packages. Installing a package may update other packages in the RA Platform and cause code failures.
CODE
12:53:37 (.env38) ~$ python
Python 3.8.12 (default, Mar 31 2022, 09:39:09) 
[GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
12:54:11 (.env38) ~$ python -m venv .env-my_new_venv
12:54:34 (.env38) ~$ source .env-my_new_venv/bin/activate
(.env-my_new_venv) mccloskey@is-mccloskey-p1:~$ pip install ...
END
- Otherwise, please ignore
# Outline
- Daily Activity Helper
  - input, datetime
- Bulk Image Organizer
  - shutil, PIL, pathlib
- Jisho API
  - requests, JSON
- EBook Writer
  - ebooklib, HTML
- Presentation Maker
  - ipynb files, nbconvert
# Use Case 1: Daily Activity Helper
- Imagine, you are sitting at your desk at Research Affiliates. It's time for morning standup and you need to have a progress report from yesterday. For that specific purpose, you have a log you keep track of:
![example_log](images/example_log.png)
- You realize you actually spend a lot of your time writing the time! If only you could easily make note of writing what you're doing, without having to figure out what time it is and write it out. It will probably save you at least 30 minutes a week.
- But you can't find the exact program that fits your needs! Well, Python can do that for you:
## Basic Time Logger
CODE
from datetime import datetime

OUTPATH = "/home/mccloskey/src/john/techforum_talk/output/my_logs.txt"

def main():
    while True:
        user_input = input("log: ")
        log = f"{datetime.now()} - {user_input}"
        with open(OUTPATH, mode="a") as f:
            f.write(f"{log}\n")
        print(log)


if __name__ == "__main__":
    main()
END
![log_output](images/log_output.png)
# Use Case 2:
- Imagine you now have a bunch of images, and you need to organize them!
![bad_images_nautilus](images/bad_images_nautilus.png)
- You could do this by hand, but if you have hundreds of images, that could take a long time.
## You can write a simple program to do make this a lot easier
- Setup:
CODE
from pathlib import Path
import shutil
from PIL import Image

input_path = Path("input")
output_path = Path("output")
output_path.mkdir(parents=True, exist_ok=True)
END
## Main Loop:
CODE
for path in input_path.iterdir():
    if path.suffix != ".jpg":
        continue
    image = Image.open(path)
    # subprocess.run(["code", path]) # for WSL, open in vscode server
    image.show()  # for Windows/Linux/Mac
    new_name = input(f"Current name: {path.stem}.\nNew name? ")
    new_path = output_path / f"{new_name}{path.suffix}"

    msg = f"Copying {path} to {new_path}. "Okay? "
    answer = input(msg).lower()

    if answer == "y":
        shutil.copyfile(path, new_path)
        print(f"Copied {path} to {new_path}. ")
    else:
        print("Not copying.")
END
## Example:
![renaming_springrolls](images/renaming_springrolls.png)
## Extending further:
- The joy of this, is that we can keep adding features. Suppose we want to sort each image by month. It turns out, that data is embedded in the image and we just need to access it.
- A quick google search shows that this can be done with the PIL library, using:
CODE
Image.open(path).getexif()
# {296: 2, 282: 72.0, 256: 4000, 257: 1824, 34853: 788, 34665: 240, 271: 'OnePlus', 
# 272: 'GM1917', 305: 'Picasa', 274: 1, 306: '2022:04:14 09:53:28', 530: (2, 2), 
# 531: 1, 283: 72.0}
END
## So we can write a quick function to extract and parse the entry for 306
CODE
def extract_month(image: Image.Image) -> typing.Optional[str]:
    metadata = image.getexif()
    if 306 not in metadata:
        return None
    timestamp_text = metadata[306]
    try:
        timestamp = datetime.strptime(timestamp_text, "%Y:%m:%d %H:%M:%S")
    except ValueError:
        return None

    return timestamp.strftime("%Y %B")
END
## And then plug that back into the main loop
CODE
month = extract_month(image)
month_path = output_path if month is None else output_path / month
month_path.mkdir(parents=True, exist_ok=True)

while True:    
    new_name = input(f"Current name: {path.stem}.\nNew name? ")
    new_path = month_path / f"{new_name}{path.suffix}"
    ...
END
## And this file is put in "2022 April":
![bounces_on_floor_example](images/bounces_on_floor_example.png)
# Use Case 3: Using an API
- I often times use a site called jisho.org
![jisho_homepage](images/jisho_homepage.png)
## Given a word or phrase, it looks up relevant Japanese/English words:
![jisho_search](images/jisho_search.png)
## But they didn't have lists like this my dictionary:
![imiwa_list_example](images/imiwa_list_example.png)
##
- But my favorite dictionary was only on iOS and I switched to using an Android phone! I needed a replacement dictionary with lists, and I found I could make one as a command line app on my computer
## So I had always dreamed of building my own, and then I learned I could easily with python!
- Jisho provides an API:
![jisho_api_firefox](images/jisho_api_firefox.png)
## This can be easily accessed with Requests:
CODE
import json

import requests
import typing as tp

BASE_URL = "https://jisho.org/api/v1/search"

def call_api(keyword: str) -> dict[str, tp.Any]:
    response = requests.get(f"{BASE_URL}/words?keyword={keyword}")
    response.raise_for_status()
    return response.json()


def main() -> None:
    keyword = input("Keyword? ")
    print(json.dumps(call_api(keyword), indent=2))


if __name__ == "__main__":
    main()
END
## This results in the same information being available with Python:
![jisho_1](images/jisho_1.png)
## And now we can work on iteratively parsing it out:
CODE
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
END
## ![jisho_2](images/jisho_2.png)
## And then ultimately, we can end up with a full command line app:
## ![og_jisho](images/og_jisho.png)
## ![og_jisho_2](images/og_jisho_2.png)
