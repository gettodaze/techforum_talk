OUTPATH = "output/my_logs_0.txt"

while True:
    user_input = input("log: ")
    with open(OUTPATH, mode="a") as f:
        print(user_input, file=f)
    print(user_input)
