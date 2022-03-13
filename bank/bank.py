import os
import pickle

from settings import pickle_file
from main import Bank

if os.path.isfile(pickle_file):
    os.remove(pickle_file)

bank = Bank()
with open(pickle_file, 'wb') as f:
    pickle.dump(bank, f)

dir_path = os.path.abspath(os.curdir)

print("Service started!\n")
while True:
    command = input("> ")
    os.system(f"python3 {dir_path}/bank/main.py {command}")
    print()
