#importing various libraries and framework common to Flask
import os
import sqlite3
from func import (
    valid_email,
    duped_username,
    valid_username,
    valid_password,
    get_password
)
from secretkey import keysec
from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import create_engine
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate
from flask_login import (
    LoginManager, 
    UserMixin,
    login_user,
    current_user,
    logout_user,
    login_required
)
#end importing

#initializing application
db = SQLAlchemy()
migrate = Migrate()
manage = LoginManager()
def creation():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'voters.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = keysec
    manage.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app
 
app = creation()
engine = create_engine("sqlite:///D:\Computer science internal assessment/voters.db")

#end initializing application

#initializing login manager



#Following the functionality of Flask-login library
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(256))

@manage.user_loader
def load(userid):
    return Users.query.get(userid)


#Avoid caching for better memory
@app.after_request
def after_request(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Expires"] = 0
    r.headers["Pragma"] = "no-cache"
    return r
#end of avoid caching


#base webpage#
@app.route("/", methods = ["GET", "POST"])
def base():
    if request.method == "GET":
        return render_template("base.html")
    elif request.method == "POST":
        if request.form.get("login") is not None:
            return redirect("/login")
        elif request.form.get("signup") is not None:
            return redirect("/register")
#end of base webpage#

#register page#
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        if (email == ""):
            email = "no email"
        if (username == "" or password ==""):
            flash("Please enter username / password")
            return redirect("/register")
        elif (not valid_username(username)):
            flash("Username too long/ contains illegal characters: space")
            return redirect("/register")
        elif (duped_username(engine, username)):
            flash("Username already exist")
            return redirect("/register")
        elif (not valid_password(password)):
            flash("password does not followed convention")
            return redirect("/register")
        elif (password != request.form.get("verify-password")):
            flash("the two passwords field do not contain the same password")
            return redirect("/register")
        elif (email != "no email" and not valid_email(email)): 
            flash("email is invalid")
            return redirect("/register")
        else:
            new = Users(
                username = username,
                password = generate_password_hash(password),
                email = email
            )
            db.session.add(new)
            db.session.commit()
            flash("Account registration success!")        
            return redirect("/")
#register page end#  

#login page#
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if (not duped_username(engine, username)):
            flash("username does not exist!")
            return redirect("/login")
        if (duped_username(engine, username)):
            if (not get_password(engine, username, password)):
                flash("username or password is incorrect!")
                return redirect("/login")
            else:
                login_user(Users.query.filter_by(username=username).first())
                flash("log in success!")
                flash(f"Welcome, {username}!")
                return redirect("/main")
#login page end#

#Contains page creation + a search bar that displays the name / id type into the search bar#
@app.route("/main", methods = ["GET", "POST"])
def contentpage():
    if request.method == "GET":
        return render_template("content.html")
    elif request.method == "POST":
        if request.form.get("make") is not None:
            return redirect("/makepoll")
        elif request.form.get("search") is not None:
            return redirect("/searchpoll")
    
@app.route("/makepoll", methods = ["GET", "POST"])
def makepoll():
    if request.method == "GET":
        return render_template("makepoll.html")
    if request.method == "POST":
        return render_template("makepoll.html")

@app.route("/searchpoll", methods = ["GET", "POST"])  
def searchpoll():
    if request.method == "GET":
        return render_template("searchpoll.html")
    if request.method == "POST":
        return render_template("searchpoll.html")
#end of mainpage# 


