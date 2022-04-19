# My Title
- John McCloskey
# Intro
Hi everyone, and welcome to my talk. I'm John McCloskey and I am on a mission to get all of you to consider using python in your everyday lives. For the non-programmers out there, I know you might think, but I don't know programming, and besides where would I ever have the opportunity to use python in my every day life? I have two answers to that.
1) It's simpler than you might expect!
2) Let us go through some examples of where you might want to use python.
# Use Case 1:
- Imagine, you are sitting at your desk at research affiliates. It's time for morning standup and you need to have a progress report from yesterday. For that specific purpose, you have a log you keep track of:
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
        with open(OUTPATH, mode="a+") as f:
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
END

## Main Loop:
CODE
for path in input_path.iterdir():
    if path.suffix != ".jpg":
        continue
    image = Image.open(path)
    # subprocess.run(["code", path]) # for WSL, open in vscode server
    image.show()  # for Windows/Linux/Mac
    while True:
        output_path.mkdir(parents=True, exist_ok=True)
        new_name = input(f"Current name: {path.stem}.\nNew name? ")
        new_path = output_path / f"{new_name}{path.suffix}"

        msg = f"Copying {path} to {new_path}. "
        if new_path.exists():
            msg += f"WARNING: {new_path} already exists. "
        answer = input(msg + "Okay? [y/n]").lower()
        if answer in {"y", "yes"}:
            shutil.copyfile(path, new_path)
            print(f"Copied {path} to {new_path}. ")
            break
        elif answer in {"n", "no"}:
            pass
        elif answer in {"s", "skip"}:
            print("Not copying.")
            break
        else:
            print(f"Invalid answer: {answer}. Must be [y]es, [n]o or [s]kip.")
END
## Example:
![renaming_springrolls](images/renaming_springrolls.png)

