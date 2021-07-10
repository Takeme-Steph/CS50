from sys import argv, exit
import csv
from cs50 import SQL

# check if 1 csv file was inputed
if len(argv) != 2:
    print("input 1 file only - Students list")
    exit(1)

# import students database
db = SQL("sqlite:///students.db")

# Open the csv filw
with open(argv[1], "r") as students:
    reader = csv.DictReader(students)
    for row in reader:
        # split name into individual parts 
        n = row["name"].split()
        # insert data into database checking if they have a middle name 
        if len(n) == 3:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       n[0], n[1], n[2], row["house"], row["birth"])
        else:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       n[0], None, n[1], row["house"], row["birth"])
