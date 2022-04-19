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

OUTPATH = "/home/mccloskey/src/john/techforum_webscraping/output/my_logs.txt"

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
