import os
import json
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API keys are set
if not os.environ.get("API_KEY"):
    raise RuntimeError("IEX API_KEY not set")
if not os.environ.get("RAVE_KEY"):
    raise RuntimeError("RAVE API_KEY not set")


@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""
    portfolio = db.execute("SELECT * FROM portfolio WHERE userid=:ids", ids=session["user_id"])

    # get current price of stocks by passing each symbol to the lookup fucntion
    j = len(portfolio)
    for i in range(j):
        p = lookup(portfolio[i]["symbol"])
        portfolio[i]["price"] = p["price"]

    # get user details
    user = db.execute("SELECT * FROM users WHERE id=:ids", ids=session["user_id"])

    return render_template("index.html", portfolio=portfolio, j=j, usd=usd, user=user)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        shares = request.form.get("shares")
        # if symbol field empty
        if not request.form.get("symbol"):
            return apology("Please input symbol")
        # if non numeric number of shares
        elif (shares.isnumeric()) == False:
            return apology("Please input a valid number of shares")
        # lookup symbol and store share value
        results = lookup(request.form.get("symbol"))
        shares = float(request.form.get("shares"))

        # if symbol not found
        if not results:
            return apology("Symbol not found")
        # if nagative numbers to buy
        elif float(shares) <= 0 or (shares.is_integer()) == False:
            return apology("Please input a valid number of shares")
        # calculate purchase price

        cost = shares * (results["price"])
        # get user data
        rows = db.execute("SELECT * FROM users WHERE id = :ids",
                          ids=session["user_id"])
        # check user has enough funds
        money = rows[0]["cash"]
        if money < cost:
            return apology("insufficient funds")
        # update db
        else:
            balance = (money - cost)
            db.execute("UPDATE users SET cash=:balance WHERE id=:ids", balance=balance, ids=session["user_id"])
            db.execute("INSERT INTO history (userid, name, symbol, price, cost, amount, type, balance) VALUES (:ids, :name, :symbol, :price, :cost, :amount, :ttype, :balance)",
                       ids=session["user_id"], name=results["name"], symbol=results["symbol"], price=results["price"], cost=cost, amount=shares, ttype="buy", balance=balance)

        # update portfolio
        port = db.execute("SELECT * FROM portfolio WHERE userid=:ids AND symbol=:symbol",ids=session["user_id"], symbol=results["symbol"])
        if not port:
            db.execute("INSERT INTO portfolio (userid,stock,amount,symbol) VALUES (:ids, :name, :amount, :symbol)", ids=session["user_id"], name=results["name"],
            amount=shares, symbol=results["symbol"])
        else:
            ntotal = port[0]["amount"]+shares
            db.execute("UPDATE portfolio SET amount=:ntotal WHERE userid=:ids AND symbol=:symbol", ntotal=ntotal, ids=session["user_id"], symbol=results["symbol"])

      # Redirect user to home page
        return redirect("/")


    else:
       return render_template("buy.html")


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM history WHERE userid=:ids",ids=session["user_id"])
    j = len(history)
    return render_template("history.html", history=history, j=j)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        usern = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = ?", usern.lower())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # if post, lookup symbol and return post page
    if request.method == "POST":
        results = lookup(request.form.get("symbol"))
        if not results:
            return apology("Symbol not found")
        else:
            return render_template("quote.html", results=results, usd=usd)

    # if get return get page
    else:
        return render_template("quote.html", typep="quote")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # submited the regsiter form
    if request.method == "POST":

        # check if a username was inputed
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # check if password was inputed
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # check if passwords match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords must match", 400)

        # check if username exists
        username = request.form.get("username")
        duplicate = db.execute("SELECT username FROM users WHERE username = :username", username=username.lower())
        if not duplicate:
            # add to database
            email = request.form.get("email")
            # check50 has an issue with blank emails, so placeholder
            if not email:
                email = "empty"
            password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            db.execute("INSERT INTO users (username, hash, email) VALUES (:username, :password, :email)", username=username.lower(), password=password, email=email)
            return redirect("/login")
        else:
            return apology("username already exists", 400)

    # get regsiter page
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # if symbol field empty
        if not symbol:
            return apology("Please input symbol")
        # if number of shares field empty
        elif shares <= 0:
            return apology("Please input a valid number of shares")

        port = db.execute("SELECT * FROM portfolio WHERE userid=:ids AND symbol=:symbol", ids=session["user_id"], symbol=symbol)
        user = db.execute("SELECT * FROM users WHERE id=:ids", ids=session["user_id"])
        # if user does not have this stock
        if not port:
            return apology("You do not own this stock")
        # if user does not have enough
        elif port[0]["amount"] < shares:
            return apology("You do not own enough shares")
        else:
            results = lookup(symbol)
            cost = results["price"] * shares
            balance = cost + user[0]["cash"]
            db.execute("UPDATE users SET cash=:balance WHERE id=:ids", balance=balance, ids=session["user_id"])
            db.execute("INSERT INTO history (userid, name, symbol, price, cost, amount, type, balance) VALUES (:ids, :name, :symbol, :price, :cost, :amount, :ttype, :balance)",
                       ids=session["user_id"], name=results["name"], symbol=results["symbol"], price=results["price"], cost=cost, amount=shares, ttype="sell", balance=balance)

            #update portfolio
            port = db.execute("SELECT * FROM portfolio WHERE userid=:ids AND symbol=:symbol", ids=session["user_id"], symbol=results["symbol"])
            if port[0]["amount"] == shares:
                db.execute("DELETE FROM portfolio WHERE userid=:ids AND symbol=:symbol", ids=session["user_id"],symbol=symbol)
            else:
                ntotal = port[0]["amount"]-shares
                db.execute("UPDATE portfolio SET amount=:ntotal WHERE userid=:ids AND symbol=:symbol", ntotal=ntotal, ids=session["user_id"], symbol=results["symbol"])

        return redirect("/")

    # get sell page with user portfolio
    else:
        portfolio = db.execute("SELECT * FROM portfolio WHERE userid=:ids", ids=session["user_id"])
        j = len(portfolio)
        return render_template("sell.html", j=j, portfolio=portfolio)


@app.route("/topup", methods=["GET", "POST"])
@login_required
def topup():
    # get topup page using Rave from flutterwave
    if request.method == "GET":
        key = os.environ.get("RAVE_KEY")
        user = db.execute("SELECT * FROM users WHERE id=:ids", ids=session["user_id"])
        return render_template("topup.html", user=user, key=key)

    # process the payment response
    else:
        response = request.get_json(force = True)
        # check if successful. Too tired to put in fraud checks lol
        if response["status"] == 'successful':
            # calculate new cash balance
            topamount = response["amount"]
            cash = db.execute("SELECT cash FROM users WHERE id=:ids", ids=session["user_id"])
            balance = float(topamount+cash[0]['cash'])
            db.execute("UPDATE users SET cash=:balance WHERE id=:ids", balance=balance, ids=session["user_id"])
            return ("200")
        else:
            return apology("Transaction failed")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
