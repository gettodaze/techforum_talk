from datetime import datetime

OUTPATH = "output/my_logs_1.txt"


def main():
    while True:
        user_input = input("log: ")
        log = f"{datetime.now()} - {user_input}"
        with open(OUTPATH, mode="a+") as f:
            f.write(f"{log}\n")
        print(log)


if __name__ == "__main__":
    main()
