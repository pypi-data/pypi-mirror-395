from time import sleep

def progress(char="#", time=5, number=10, end_char=""):
    delay = time / number
    for _ in range(number):
        sleep(delay)
        print(char, end="", flush=True)
    print(end_char)

def ml_progress(char="#", time=5, number=10, end_char=""):
    delay = time / number
    for i in range(1, number + 1):
        print(char * i)
        sleep(delay)
    print(end_char)
