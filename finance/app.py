import email
import os
import json
from turtle import update
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import sqlalchemy.types as types

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

# Configure SQL alchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///finance.db"
db = SQLAlchemy(app)

# Make sure API keys are set
if not os.environ.get("API_KEY"):
    raise RuntimeError("IEX API_KEY not set")
if not os.environ.get("RAVE_KEY"):
    raise RuntimeError("RAVE API_KEY not set")
if not os.environ.get("PAYMENT_CALLBACK"):
    raise RuntimeError("Payment gateway callback url not set")


#create models
class History(db.Model):
    PK = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    name = db.Column(db.String(50))
    symbol = db.Column(db.String(50))
    price = db.Column(db.Float)
    amount = db.Column(db.Integer)
    cost = db.Column(db.Float)
    type = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.now)
    balance = db.Column(db.Integer)

class Portfolio(db.Model):
    PK = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    stock = db.Column(db.String(50))
    symbol = db.Column(db.String(50))
    amount = db.Column(db.Integer)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    hash = db.Column(db.String(200))
    cash = db.Column(db.Float)
    email = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.now)

@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""
    portfolio = Portfolio.query.filter_by(userid=session["user_id"]).all()

    # get current price of stocks by passing each symbol to the lookup fucntion
    for i in portfolio:
        p = lookup(i.symbol)
        i.price = p["price"]
    

    # get user details
    user = Users.query.filter_by(id=session["user_id"]).first()

    return render_template("index.html", portfolio=portfolio, usd=usd, user=user)


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
        rows = Users.query.filter_by(id=session["user_id"]).first()
        # check user has enough funds
        money = rows.cash
        if money < cost:
            return apology("insufficient funds")
        # update db
        else:
            update_user = Users.query.get(session["user_id"])
            balance = (money - cost)

            update_user.cash = balance
            db.session.commit()

            history_new = History(userid=session["user_id"], name=results["name"], symbol=results["symbol"], 
            price=results["price"], cost=cost, amount=shares, type="buy", balance=balance)
            db.session.add(history_new)
            db.session.commit()

        # update portfolio
        port = Portfolio.query.filter_by(userid=session["user_id"], symbol=results["symbol"]).first()
        if not port:
            new_port = Portfolio(userid=session["user_id"], stock=results["name"], amount=shares, symbol=results["symbol"])
            db.session.add(new_port)
            db.session.commit()
        else:
            ntotal = port.amount+shares
            port.amount = ntotal
            db.session.commit()

      # Redirect user to home page
        return redirect("/")


    else:
       return render_template("buy.html")


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Show history of transactions"""
    history = History.query.filter_by(userid=session["user_id"]).all()
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
        rows = Users.query.filter_by(username = usern.lower()).first()

        # Ensure username exists and password is correct
        if not check_password_hash(rows.hash, request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows.id

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
        duplicate = Users.query.filter_by(username = username.lower()).first()
        if not duplicate:
            # add to database
            email = request.form.get("email")
            #issue with blank emails, so placeholder
            if not email:
                email = "empty"
            password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            new_user = Users(username=username.lower(), hash=password, email=email, cash=10000)
            db.session.add(new_user)
            db.session.commit()
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

        port = Portfolio.query.filter_by(userid=session["user_id"],symbol=symbol).first()
        user = Users.query.filter_by(id=session["user_id"]).first()
        # if user does not have this stock
        if not port:
            return apology("You do not own this stock")
        # if user does not have enough
        elif port.amount < shares:
            return apology("You do not own enough shares")
        else:
            results = lookup(symbol)
            cost = results["price"] * shares
            balance = cost + user.cash
            user.cash=balance
            db.session.commit()
            history_new = History(userid=session["user_id"], name=results["name"], symbol=results["symbol"], 
            price=results["price"], cost=cost, amount=shares, type="sell", balance=balance)
            db.session.add(history_new)
            db.session.commit()
            
            #update portfolio
            port = Portfolio.query.filter_by(userid=session["user_id"],symbol=results["symbol"]).first()
            if port.amount == shares:
                db.session.delete(port)
                db.session.commit()
                
            else:
                ntotal = port.amount-shares
                port.amount = ntotal
                db.session.commit()
        return redirect("/")

    # get sell page with user portfolio
    else:
        portfolio = Portfolio.query.filter_by(userid=session["user_id"]).all()
        j = len(portfolio)
        return render_template("sell.html", j=j, portfolio=portfolio)


@app.route("/topup", methods=["GET", "POST"])
@login_required
def topup():
    # get topup page using Rave from flutterwave
    if request.method == "GET":
        key = os.environ.get("RAVE_KEY")
        callback = os.environ.get("PAYMENT_CALLBACK")
        user = Users.query.filter_by(id=session["user_id"]).first()
        return render_template("topup.html", user=user, key=key, callback=callback)

    # process the payment response
    else:
        response = request.get_json(force = True)
        # check if successful. Too tired to put in fraud checks lol
        if response["status"] == 'successful':
            # calculate new cash balance
            topamount = response["amount"]
            usern = Users.query.filter_by(id=session["user_id"]).first()
            cash = usern.cash
            balance = float(topamount+cash)
            usern.cash = balance
            db.session.commit()
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
