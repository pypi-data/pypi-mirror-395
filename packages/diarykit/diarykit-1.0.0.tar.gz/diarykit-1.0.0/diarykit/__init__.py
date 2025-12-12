from hashlib import *
from cryptography.fernet import Fernet
from tkinter import *
from random import *
from time import *
from sys import *
set_int_max_str_digits(999999999)
key = input("Type your pin or say NU for new user: ")
if key.strip().upper() == "NU":
    with open("keys.txt", "ab") as f:
        rand_num = str(randint(1000, 9999))
        with open("keys.txt", "rb") as ff:
            while sha256(rand_num.encode()).hexdigest() in ff.read().splitlines():
                rand_num = str(randint(1000, 9999))
        f.write(sha256(rand_num.encode()).hexdigest().encode() + b"\n")
        key = Fernet.generate_key() + b"\n"
        f.write(key)
        print(f"{rand_num} is your pin. Remember this to access your diary!")
    with open(f"{int(rand_num) * 1212 / 11}_diary.txt", "w") as f:
        print("Your diary was successfully created!")
else:
    rand_num = key
    hexfnum = sha256(key.encode()).hexdigest()
    with open("keys.txt", "rb") as f:
        file = f.read().splitlines()
        key = file.index(hexfnum.encode())
        key = file[int(key) + 1]
rorw = input("Do you want to read your diary or write it? (r/w)").lower().strip()
if rorw == "w":
    with open(f"{int(rand_num) * 1212 / 11}_diary.txt", "ab") as d:
        d.write(Fernet(key).encrypt(strftime("%D\n%T").encode()) + b"\n")
        print("Type your diary entry and type 'end' in the end (time and date will be taken automatially):")
        line = ""
        lines = []
        while True:
            line = input()
            if line.lower() == "end":
                break
            d.write(Fernet(key).encrypt(line.encode()) + b"\n")
        rating = input("How much would you rate the day an a scale of 1-3? ").strip()
        if rating == "1":
            rating = ":("
        elif int(rating.strip()) < 1:
            rating = ":("
        elif rating == "2":
            rating = ":|"
        elif rating == "3":
            rating = ":)"
        elif int(rating.strip()) > 3:
            rating = ":)"
        d.write(Fernet(key).encrypt(f"What I thought of the day: {rating}".encode()))
        d.write(b"\n\n")
        for line in lines:
            d.write(line)
elif rorw == "r":
    with open(f"{int(rand_num) * 1212 / 11}_diary.txt", "rb") as f:
        for line in f:
            if line != b"\n":
                print(Fernet(key.strip()).decrypt(line).decode())
            else:
                print()
