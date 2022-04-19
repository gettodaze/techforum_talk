import os
from pathlib import Path
import shutil
import subprocess
from PIL import Image
from datetime import datetime

input_path = Path("/home/mccloskey/src/techforum_talk/input")
output_path = Path("/home/mccloskey/src/techforum_talk/output")

for path in input_path.iterdir():
    image = Image.open(path)
    subprocess.run(["code", path]) # for WSL, open in vscode server
    metadata = image.getexif()
    print(metadata)
    try:
        timestamp_text = metadata[306]
        timestamp = datetime.strptime(timestamp_text, "%Y:%m:%d %H:%M:%S")
        month = timestamp.strftime('%Y %B')
    except (KeyError, ValueError):
        month = None
    # image.show() # for Windows/Linux/Mac
    while True:
        month_path = output_path if month is None else output_path / month
        month_path.mkdir(parents=True, exist_ok=True)
        new_name = input(f'Current name: {path.stem}.\nNew name? ')
        new_path = month_path / f'{new_name}{path.suffix}'

        msg = f"Copying {path} to {new_path}. "
        if new_path.exists():
            msg += f'WARNING: {new_path} already exists. '
        answer = input(msg+'Okay? [y/n]').lower()
        if answer in {'y', 'yes'}:
            shutil.copyfile(path, new_path)
            print(f"Copied {path} to {new_path}. ")
            break
        elif answer in {'n', 'no'}:
            pass
        elif answer in {'s', 'skip'}:
            print('Not copying.')
            break
        else:
            print(f'Invalid answer: {answer}. Must be [y]es, [n]o or [s]kip.')
