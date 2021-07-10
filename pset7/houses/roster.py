from sys import argv, exit
from cs50 import SQL

# check if house name was inputed
if len(argv) != 2:
    print("Please input house name only")
    exit(1)

# import students database
db = SQL("sqlite:///students.db")

# Query database and store results in a dict
roaster = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", argv[1])

# print results checking for null middle name
for row in roaster:
    if row['middle'] == None:
        print("{} {}, born in {}".format(row['first'], row['last'], row['birth']))
    else:
        print("{} {} {}, born in {}".format(row['first'], row['middle'], row['last'], row['birth']))
