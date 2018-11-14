import subprocess
from tempfile import gettempdir
import sqlite3
import os
from time import sleep

PATH_TO_DB = gettempdir() + "//program_killer//main.db"


def kill():
    while True:
        if os.path.isfile(PATH_TO_DB):
            conn = sqlite3.connect(PATH_TO_DB)
            c = conn.cursor()
            c.execute("SELECT * FROM VICTIMS")
            rows = c.fetchall()
            conn.close()
            if rows is not []:
                for row in rows:
                    try:
                        subprocess.Popen(args="taskkill /im \"" + str(row[1]) + "\" /f", stdout=subprocess.PIPE,
                                         shell=False)
                    except:
                        pass
        sleep(1)


def check():
    try:
        raw = subprocess.Popen(args="powershell -Command \"Get-Process kill\"", stdout=subprocess.PIPE,
                         shell=False)
        info = raw.stdout.read(-1)
        if b"Cannot find a process with the name \"kill\"" in info:
            return False
        else:
            return True
    except:
        pass


if __name__ == '__main__':
    if not check():
        kill()

