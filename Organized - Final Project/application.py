import os
import json
from flask import Flask, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, usd, datetime_format
from datetime import datetime

# Configure application
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filters
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["datetime_format"] = datetime_format


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure app to use SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
db = SQLAlchemy(app)



#create models
class Todos(db.Model):
    PK = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))
    assigned_to = db.Column(db.String(50))
    cost = db.Column(db.Float)
    status = db.Column(db.String(50))
    due_date = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.now)
    umbrellasid = db.Column(db.Integer)

class Umbrellas(db.Model):
    PK = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))
    title = db.Column(db.String(50))
    budget = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.now)
    eventsid = db.Column(db.Integer)

class Events(db.Model):
    PK = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))
    title = db.Column(db.String(50))
    budget = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.now)
    userid = db.Column(db.Integer)

class Users(db.Model):
    PK = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(100))
    email = db.Column(db.String(100), default="empty")
    date_created = db.Column(db.DateTime, default=datetime.now)



# some code was borrowed from https://codeloop.org/flask-crud-application-with-sqlalchemy/
@app.route("/todo", methods=["GET", "POST"])
@login_required
def todo():
    """Show all TODO items and store new TODO items"""
    #redirect to homepage if it has no query
    if not request.args.get("umbrella"):
        return redirect("/")

    umbrellaID = request.args.get("umbrella")

    #check if todos belong to this user
    umbrella=Umbrellas.query.filter_by(PK=umbrellaID).first()
    if not umbrella:
        return redirect("/")

    event=Events.query.filter_by(PK=umbrella.eventsid, userid=session["user_id"]).first()
    if not event:
        return redirect("/")

    if request.method == "POST":
        #store new todo item in db
        if request.form.get("event")=="add":
            item = Todos(description=request.form.get("description"), assigned_to=request.form.get("assigned_to"), cost=request.form.get("cost"),
            status=request.form.get("status"), umbrellasid=umbrellaID)
            if request.form.get("due_date"):
                    item.due_date=datetime.strptime(request.form.get("due_date"), '%Y-%m-%dT%H:%M')
            db.session.add(item)
            db.session.commit()
            flash("Todo added Successfully")

        #edit todo item
        elif request.form.get("event")=="edit":
            update_todo = Todos.query.get(request.form.get('PK'))
            if not request.form.get("PK") or not update_todo:
                return "Record not found"
            else:
                update_todo.description=request.form.get("description")
                update_todo.assigned_to=request.form.get("assigned_to")
                update_todo.cost=request.form.get("cost")
                update_todo.status=request.form.get("status")
                if update_todo.due_date:
                    update_todo.due_date=datetime.strptime(request.form.get("due_date"), '%Y-%m-%dT%H:%M')
                if not update_todo.cost:
                    update_todo.cost = 0
                db.session.commit()
                flash("Todo Updated Successfully")

        #delete todo item
        elif request.form.get("event")=="delete":
            if not request.form.get("PK"):
                return "Record not found"
            else:
                delete_todo = Todos.query.get(request.form.get('PK'))
                db.session.delete(delete_todo)
                db.session.commit()
                flash("Todo Deleted Successfully")

        #display updated todo list
        todos = Todos.query.filter_by(umbrellasid=umbrellaID).all()
        return render_template("todo.html", todos=todos, umbrella=umbrella)

    else:
        #display todo list
        todos = Todos.query.filter_by(umbrellasid=umbrellaID).all()
        return render_template("todo.html", todos=todos, umbrella=umbrella)


@app.route("/umbrella", methods=["GET", "POST"])
@login_required
def umbrella():
    """Show all Umbrellas and store new Umbrellas"""

    #redirect to homepage if it has no query
    if not request.args.get("event"):
        return redirect("/")

    eventID = request.args.get("event")

    #check if umbrellas belong to this user
    event=Events.query.filter_by(PK=eventID, userid=session["user_id"]).first()
    if not event:
        return redirect("/")

    if request.method == "POST":
        #store new umbrella in db
        if request.form.get("event")=="add":
            item = Umbrellas(description=request.form.get("description"),title=request.form.get("title"), budget=request.form.get("budget"),
            eventsid=eventID)
            db.session.add(item)
            db.session.commit()
            flash("Umbrella added Successfully")

        #edit umbrella
        elif request.form.get("event")=="edit":
            if not request.form.get("PK"):
                return "Record not found"
            else:
                update_umbrela = Umbrellas.query.get(request.form.get('PK'))
                update_umbrela.description=request.form.get("description")
                update_umbrela.title=request.form.get("title")
                update_umbrela.budget=request.form.get("budget")
                if not update_umbrela.budget:
                    update_umbrela.budget = 0
                db.session.commit()
                flash("Umbrella Updated Successfully")

        #delete umbrella
        elif request.form.get("event")=="delete":
            if not request.form.get("PK"):
                return "Record not found"
            else:
                delete_umbrella = Umbrellas.query.get(request.form.get('PK'))
                todos = Todos.query.filter_by(umbrellasid=delete_umbrella.PK).all()

                #delete all todos for the umbrella
                for todo in todos:
                    db.session.delete(todo)
                    db.session.commit()

                #delete umbrella
                db.session.delete(delete_umbrella)
                db.session.commit()
                flash("Umbrella Deleted Successfully")

        #display updated umbrella list

        umbrellas = Umbrellas.query.filter_by(eventsid=eventID).all()
        return render_template("umbrella.html", umbrellas=umbrellas, event=event)

    else:
        #display umbrella list
        umbrellas = Umbrellas.query.filter_by(eventsid=eventID).all()
        return render_template("umbrella.html", umbrellas=umbrellas, event=event)


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show all Events and store new Events"""

    if request.method == "POST":
        #store new event in db
        if request.form.get("event")=="add":
            item = Events(description=request.form.get("description"),title=request.form.get("title"), budget=request.form.get("budget"), userid=session["user_id"])
            db.session.add(item)
            db.session.commit()
            flash("Event added Successfully")

        #edit event
        elif request.form.get("event")=="edit":
            if not request.form.get("PK"):
                return "Record not found"
            else:
                update_event = Events.query.get(request.form.get('PK'))
                update_event.description=request.form.get("description")
                update_event.title=request.form.get("title")
                update_event.budget=request.form.get("budget")
                if not update_event.budget:
                    update_event.budget = 0
                db.session.commit()
                flash("Event Updated Successfully")

        #delete event
        elif request.form.get("event")=="delete":
            if not request.form.get("PK"):
                return "Record not found"
            else:
                delete_event = Events.query.get(request.form.get('PK'))
                umbrellas = Umbrellas.query.filter_by(eventsid=delete_event.PK).all()

                #delete all umbrellas for the events
                for umbrella in umbrellas:
                    #delete all todos for the umbrella
                    todos = Todos.query.filter_by(umbrellasid=umbrella.PK).all()
                    for todo in todos:
                        db.session.delete(todo)
                        db.session.commit()

                    db.session.delete(umbrella)
                    db.session.commit()

                #delete event
                db.session.delete(delete_event)
                db.session.commit()
                flash("Event Deleted Successfully")

        #display updated todo list
        events = Events.query.filter_by(userid=session["user_id"]).all()
        return render_template("index.html", events=events)

    else:
        #display todo list
        events = Events.query.filter_by(userid=session["user_id"]).all()
        return render_template("index.html", events=events)


@app.route("/login", methods=["GET", "POST"])
def login():

    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        username = request.form.get("username").lower()
        user = Users.query.filter_by(username=username).first()

        # Ensure username exists and password is correct
        if not user or not check_password_hash(user.password_hash, request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = user.PK

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


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
        username = request.form.get("username").lower()
        user = Users.query.filter_by(username=username).first()
        if not user:
            # add to database
            password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            user = Users(username=username,email=request.form.get("email"), password_hash=password)
            db.session.add(user)
            db.session.commit()
            flash("User Created Successfully")

            # Redirect user to home page
            return redirect("/login")

        else:
            return apology("username already exists", 400)

    # get regsiter page
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
