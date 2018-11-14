import os
import sys
from tempfile import gettempdir
from colorama import Fore, Style, init
import sqlite3
from itertools import chain


def print_out(string, _type, end="\n"):
    if _type != "":
        if string != "":
            if _type == "error":
                print(Fore.RED + string, Style.RESET_ALL, end=end)
            elif _type == "success":
                print(Fore.LIGHTGREEN_EX + string, Style.RESET_ALL, end=end)
            elif _type == "warning":
                print(Fore.YELLOW + string, Style.RESET_ALL, end=end)
            elif _type == "normal":
                print(Fore.WHITE + string, end=end)


class ProgramKiller:
    def __init__(self):
        self.PATH = gettempdir() + "//program_killer"
        self.TABLE = '''CREATE TABLE VICTIMS
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL);'''
        self.HELP = {'Help:': 'Shows this help message.',
                     '-a, --add': 'Adds the program to database.',
                     '-r, --remove': 'Removes the program from database.',
                     'value': 'The program to perform action on.',
                     '-s, --show': 'Shows the programs stored in database.',
                     '--create-db': 'Creates the database.',
                     '--del-db': 'Deletes the database.',
                     '--del-all': 'Deletes all the records from database.'
                     }
        self.HEADER = sys.argv[0] + " [-a|--add || -r|--remove] \"value\" [-s|--show] "
        self.checks()

    def checks(self):
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)
            if not os.path.isfile(self.PATH + "//main.db"):
                self.create_db()

    def print_help(self):
        print_out("Usage:", "success")
        print_out("  " + self.HEADER, "normal")
        for cmd, v in self.HELP.items():
            print("\n" + Fore.WHITE + cmd + ":\n\t" + Fore.YELLOW + v + Style.RESET_ALL)

    def del_all(self):
        conn = sqlite3.connect(self.PATH + "//main.db")
        c = conn.cursor()
        c.execute("DELETE FROM VICTIMS ")
        conn.commit()
        conn.close()
        print_out("[+] Database truncated successfully.", "success")

    def fetch_data(self):
        if os.path.isfile(self.PATH + "//main.db"):
            conn = sqlite3.connect(self.PATH + "//main.db")
            c = conn.cursor()
            c.execute("SELECT * FROM VICTIMS")
            rows = c.fetchall()
            conn.close()
            if rows is []:
                return None
            else:
                return rows
        else:
            print_out("[-] Database does not exists.", "error")

    def del_db(self):
        if os.path.exists(self.PATH):
            if os.path.isfile(self.PATH + "//main.db"):
                os.remove(self.PATH + "//main.db")
                print_out("[+] Database deleted successfully.", "success")
            else:
                print_out("[*] No Database exists.", "warning")
        else:
            print_out("[-] Path to file does not exists.", "error")

    def create_db(self):
        if os.path.exists(self.PATH):
            if not os.path.isfile(self.PATH + "//main.db"):
                conn = sqlite3.connect(self.PATH + "//main.db")
                c = conn.cursor()
                c.execute(self.TABLE)
                conn.commit()
                conn.close()
                print_out("[+] Database created successfully.", "success")
            else:
                print_out("[*] Database already exists.", "warning")
        else:
            print_out("[-] Path to file does not exists.", "error")

    def check_db(self):
        if os.path.exists(self.PATH):
            if os.path.isfile(self.PATH + "//main.db"):
                print_out("[*] Database exists.", "warning")
                return None
        print_out("[*] Database does not exists.", "warning")

    def execution(self, value, operation):
        if os.path.exists(self.PATH):
            if os.path.isfile(self.PATH + "//main.db"):
                if operation == "a":
                    rows = self.fetch_data()
                    if rows is None or value not in chain(*rows):
                            conn = sqlite3.connect(self.PATH + "//main.db")
                            c = conn.cursor()
                            c.execute("INSERT INTO VICTIMS(NAME) VALUES(\'" + value + "\')")
                            conn.commit()
                            conn.close()
                            print_out("[+] Value Added Successfully!", "success")
                    else:
                        print_out("[*] \'" + value + "\' already exists in DB.", "warning")

                elif operation == "r":
                    rows = self.fetch_data()
                    if value in chain(*rows):
                        conn = sqlite3.connect(self.PATH + "//main.db")
                        c = conn.cursor()
                        c.execute("DELETE FROM VICTIMS WHERE NAME=\'" + value + "\'")
                        conn.commit()
                        conn.close()
                        print_out("[+] Value Removed Successfully!", "success")
                    else:
                        print_out("[*] \'" + value + "\' not found.", "warning")
            else:
                print_out("[-] Database does not exists.", "error")
        else:
            print_out("[-] Path to file does not exists.", "error")

    def show_items(self):
        rows = self.fetch_data()
        if rows is not None:
            print_out("ID\tNAME", "normal")
            print_out("-" * 40, "warning")
            for row in rows:
                print_out(str(row[0]), "normal", end='\t')
                print_out(str(row[1]), "normal")


def main():
    pk = ProgramKiller()

    try:
        if len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
            pk.print_help()
        elif sys.argv[1] == "-a" or sys.argv[1] == "--add":
            pk.execution(sys.argv[2], "a")
        elif sys.argv[1] == "-r" or sys.argv[1] == "--remove":
            pk.execution(sys.argv[2], "r")
        elif sys.argv[1] == "-s" or sys.argv[1] == "--show":
            pk.show_items()
        elif sys.argv[1] == "--del-db":
            pk.del_db()
        elif sys.argv[1] == "--create-db":
            pk.create_db()
        elif sys.argv[1] == "--del-all":
            pk.del_all()
        elif sys.argv[1] == "--check-db":
            pk.check_db()
    except IndexError:
        print_out("[*] Parameter \'value\' missing.\n", "warning")
        print_out("Usage:", "success")
        print_out("  " + pk.HEADER, "normal")


if __name__ == '__main__':
    init()
    main()
