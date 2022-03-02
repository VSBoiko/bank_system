import sys
import os

dir_path = os.path.abspath(os.curdir)

print("Service started!\n")
while True:
    command = input("> ")
    os.system(f"python3 {dir_path}/main.py {command}")
    print()
