import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        #Add the user's entry into the database
        name = request.form.get("name")
        day = request.form.get("day")
        month = request.form.get("month")
        db.execute("INSERT INTO birthdays (name, day, month) VALUES (:name, :day, :month)", name=name, day=day, month=month)
        return redirect("/")

    else:

        # Display the entries in the database on index.html
        rows = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", rows=rows)

#Delete entries by id number
@app.route("/delete", methods=["POST"])
def delete():
    ids = request.form.get("ids")
    db.execute("DELETE FROM birthdays WHERE id = :ids", ids=ids)
    return redirect("/")

#Edit entries by id number
@app.route("/edit", methods=["POST"])
def edit():
    if request.method == "POST":
        name = request.form.get("name")
        day = request.form.get("day")
        month = request.form.get("month")
        ids = request.form.get("ids")
        db.execute("UPDATE birthdays SET name = :name, day = :day, month = :month WHERE id = :ids", name=name, day=day, month=month, ids=ids)
        return redirect("/")
