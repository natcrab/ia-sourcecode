#importing various libraries and framework common to Flask
import os
import sqlite3
import math
from func import (
    valid_email,
    duped_username,
    valid_username,
    valid_password,
    get_password,
    duped_pollId,
    getUsername,
    optioncountarr
)
from voting import(
    getpoll,
    checkvoted,
    optvoted,
    tallying,
    addCounter,
    searchres,
    pollpassword,
    whovoted,
    pollpopularity
)
from secretkey import keysec
from datetime import datetime, timedelta
from flask import Flask, redirect, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text
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

class Polls(db.Model):
    pollId = db.Column(db.String, primary_key=True, unique = True)
    creator = db.Column(db.String(20))
    pollname = db.Column(db.String)
    pollDescription = db.Column(db.String)
    pollQuestion = db.Column(db.String) #index 4
    privacyMode = db.Column(db.String)
    votingMode = db.Column(db.String)
    publicity = db.Column(db.Boolean)
    pollTime = db.Column(db.Integer) #index 9
    pollManual = db.Column(db.Boolean)
    currentWinner = db.Column(db.String)
    NumofOptions = db.Column(db.Integer)
    needPassword = db.Column(db.Boolean)
    password = db.Column(db.String(200)) #index14
    ongoing = db.Column(db.Boolean)
    option1 = db.Column(db.String) #index 16
    option1exp = db.Column(db.String)
    option2 = db.Column(db.String)
    option2exp = db.Column(db.String)
    option3 = db.Column(db.String)
    option3exp = db.Column(db.String)
    option4 = db.Column(db.String)
    option4exp = db.Column(db.String)
    option5 = db.Column(db.String)
    option5exp = db.Column(db.String)
    option6 = db.Column(db.String)
    option6exp = db.Column(db.String)
    option7 = db.Column(db.String)
    option7exp = db.Column(db.String)
    option8 = db.Column(db.String)
    option8exp = db.Column(db.String)
    option9 = db.Column(db.String)
    option9exp = db.Column(db.String)
    option10 = db.Column(db.String)
    option10exp = db.Column(db.String)


class Votes(db.Model):
    Counter = db.Column(db.Integer, primary_key = True, unique = True)
    Userid = db.Column(db.Integer)
    pollid = db.Column(db.String)
    voteoption = db.Column(db.String)
    

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

@app.route("/", methods = ["GET", "POST"])
def startup():
    if request.method == "GET":
        return redirect("/home")
    else:
        return "Oops, you aren't supposed to be here. It seems something had gone wrong"

#base webpage#
@app.route("/home", methods = ["GET", "POST"])
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
            return redirect("/home")
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
                login_user(Users.query.filter(func.lower(Users.username)==username.lower()).first())
                flash("log in success!")
                flash(f"Welcome, {getUsername(engine, username)}!")
                return redirect("/main")
#login page end#

#Contains page creation + a search bar that displays the name / id type into the search bar#
@login_required
@app.route("/main", methods = ["GET", "POST"])
def contentpage():
    if request.method == "GET":
        return render_template("content.html")
    elif request.method == "POST":
        if request.form.get("make") is not None:
            return redirect("/main/makepoll")
        elif request.form.get("search") is not None:
            return redirect("/main/searchpoll")
        elif request.form.get("logout") is not None:
            logout_user()
            return redirect("/home")
        elif request.form.get("Return") is not None:
            return redirect("/main")

@login_required    
@app.route("/main/makepoll", methods = ["GET", "POST"])
def makepoll():
    if request.method == "GET":
        return render_template("pollinit.html")
    if request.method == "POST":
        if request.form.get("makepoll") is not None:
            optioncount = int(request.form.get("optionsnum"))
            needPass = int(request.form.get("passwordReq"))
            if optioncount > 10 or optioncount<2:
                flash("Please enter a number between two and ten")
                return render_template("pollinit.html")
            else:
                return render_template("makepoll.html", optioncount = optioncountarr(optioncount), numopt = optioncount, needPass = needPass)
        elif request.form.get("create") is not None:
            optionsarr = ["option1", "option2", "option3", "option4", "option5", "option6","option7","option8","option9","option10"]
            explainsarr = ["explain1", "explain2","explain3","explain4","explain5","explain6","explain7","explain8","explain9","explain10",]
            pollOptions = []
            pollExplains = []
            optioncount = int(request.form.get("optcount"))
            needPass = int(request.form.get("passwordNeeded"))
            for i in range(optioncount):
                temp = request.form.get(optionsarr[i])
                if temp in pollOptions or temp == "":
                    flash("The poll options cannot be repeated or be empty")
                    return render_template("makepoll.html", optioncount = optioncountarr(optioncount), numopt = optioncount, needPass = needPass)
                pollOptions.append(temp)
                temp = request.form.get(explainsarr[i])
                pollExplains.append(temp)
            while len(pollOptions) < 10:
                pollOptions.append("")
                pollExplains.append("")
            pollId = str(request.form.get("pollId"))
            pollId = pollId.lower()
            timerSeconds = int(request.form.get("timerDay"))*86400+int(request.form.get("timerHours"))*3600+int(request.form.get("timerMinutes"))*60+int(request.form.get("timerSeconds"))
            manuality = False
            if (request.form.get("pollPublicity")) == "1":
                isPublic = True
            else:
                isPublic = False
            if timerSeconds <= 0:
                manuality = True
            if duped_pollId(engine, pollId):
                flash("poll Id already used, please pick another one")
                return render_template("makepoll.html", optioncount = optioncountarr(optioncount), numopt = optioncount, needPass = needPass)
            else:
                if needPass == 1:
                    needPassBool = True
                    password = str(request.form.get("pollPassword"))
                    password = generate_password_hash(password)
                else:
                    needPassBool = False
                    password = ""
                new = Polls(
                    pollId = pollId,
                    creator = current_user.username,
                    pollname = request.form.get("pollName"),
                    pollDescription = request.form.get("pollDesc"),
                    pollQuestion = request.form.get("pollQuestion"),
                    privacyMode = request.form.get("pollPrivacy"),
                    votingMode = request.form.get("voteSystem"),
                    publicity = isPublic,
                    pollTime = datetime.now() + timerSeconds,
                    pollManual = manuality,
                    currentWinner = pollOptions[0],
                    NumofOptions = optioncount,
                    ongoing = True,
                    needPassword = needPassBool,
                    password = password,
                    option1 = pollOptions[0], 
                    option1exp = pollExplains[0],
                    option2 = pollOptions[1], 
                    option2exp = pollExplains[1],
                    option3 = pollOptions[2], 
                    option3exp = pollExplains[2],
                    option4 = pollOptions[3], 
                    option4exp = pollExplains[3],
                    option5 = pollOptions[4], 
                    option5exp = pollExplains[4],
                    option6 = pollOptions[5], 
                    option6exp = pollExplains[5],
                    option7 = pollOptions[6], 
                    option7exp = pollExplains[6],
                    option8 = pollOptions[7], 
                    option8exp = pollExplains[7],
                    option9 = pollOptions[8], 
                    option9exp = pollExplains[8],
                    option10 = pollOptions[9], 
                    option10exp = pollExplains[9]
                )
                db.session.add(new)
                db.session.commit()
                flash("Poll added to database!")
                return redirect("/main")
            



@login_required
@app.route("/main/searchpoll/", methods = ["GET", "POST"])  
def searchpoll():
    if request.method == "GET":
        return render_template("searchpoll.html")
    if request.method == "POST":
        if request.form.get("pollIdButton") is not None:
            if not duped_pollId(engine, request.form.get("searchPollId")):
                flash("No such poll ID!")
                return render_template("searchpoll.html")
            else:
                result = request.form.get("searchPollId")
                return redirect(url_for("pollDisplay", pollId = result))
        if request.form.get("pollNameButton") is not None:
            return redirect("/main/polls")

@login_required
@app.route("/main/polls", methods = ["GET", "POST"])
def searchresults():
    if request.method == "GET":
        results = searchres(engine, "")
        toDisplay = []
        for i in results:
            toDisplay.append(getpoll(engine, i))
            n = len(toDisplay)
            for i in range(math.floor(n/2)):
                        temp = toDisplay[i]
                        toDisplay[i] = toDisplay[n-1-i]
                        toDisplay[n-1-i] = temp
        return render_template("pollfind.html", toDisplay = toDisplay)
    if request.method == "POST":
        if request.form.get("searchPollName") is not None:
            results = searchres(engine, request.form.get("searchbar"))
            toDisplay = []
            for i in results:
                toDisplay.append(getpoll(engine, i))
            x = request.form.getlist("status")
            try:
                if "ongoing" not in x:   
                    for i in range(len(toDisplay)):
                        if toDisplay[i][15] == True:
                            toDisplay[i] = "rm"
                if "ended" not in x:   
                    for i in range(len(toDisplay)):
                        if toDisplay[i][15] == False:
                            toDisplay[i] = "rm" 
            except(IndexError):
                pass
            finally:  
                while "rm" in toDisplay:
                    toDisplay.remove("rm")     
                sortmode = request.form.get("searchSort")
                match sortmode:
                    case "New":
                        n = len(toDisplay)
                        for i in range(math.floor(n/2)):
                            temp = toDisplay[i]
                            toDisplay[i] = toDisplay[n-1-i]
                            toDisplay[n-1-i] = temp
                    case "Popularity":
                        length = len(toDisplay)
                        for i in range(length):
                            for k in range(0, length - i - 1, 1):
                                if pollpopularity(engine, toDisplay[k][0]) < pollpopularity(engine, toDisplay[k+1][0]):
                                    temp = toDisplay[k] 
                                    toDisplay[k] = toDisplay[k+1]
                                    toDisplay[k+1] = temp
                    case _:
                        pass                
                return render_template("pollfind.html", toDisplay = toDisplay)
        else:
            numofPolls = int(request.form.get("numofDisplay"))
            for i in range(numofPolls):
                if request.form.get("".join(["visitPoll", str(i+1)])) is not None:
                    pollId = request.form.get("".join(["visitPollId", str(i+1)]))
                    return redirect(url_for("pollDisplay", pollId = pollId))



@login_required
@app.route("/main/polls/<pollId>", methods = ["GET", "POST"])
def pollDisplay(pollId):
    pollData = getpoll(engine, pollId)
    passEntered = False
    if current_user.username == pollData[1]:
        isOwner = True
        passEntered = True
    else:
        isOwner = False
    if pollData[15]:
        if request.method == "GET":
            return render_template("polldata.html", pollData = pollData, voted = checkvoted(engine, current_user.id, pollId), optvoted = "".join(list(optvoted(engine, current_user.id, pollId))[6:]), isOwner = isOwner, passEntered = passEntered)
        if request.method == "POST":
            if request.form.get("pollPassButton") is not None:
                password = request.form.get("pollPass")
                if pollpassword(engine, pollId, password):                   
                    return render_template("polldata.html", pollData = pollData, voted = checkvoted(engine, current_user.id, pollId), optvoted = "".join(list(optvoted(engine, current_user.id, pollId))[6:]), isOwner = isOwner, passEntered= True)
                else:
                    flash("Wrong password, please try again")
                    return redirect(url_for("pollDisplay", pollId = pollId))
            if request.form.get("endpoll") is not None:
                with engine.connect() as connection:
                    connection.execute(text("UPDATE Polls Set ongoing = False WHERE pollid = :pollid"), {'pollid': pollId})
                    connection.commit()
                redirect(url_for("pollDisplay", pollId = pollId))
            if pollData[6] == "popularity":
                for i in range(pollData[12]):
                    if request.form.get("".join(["option", str(i+1)])) is not None:
                        if checkvoted(engine, current_user.id, pollId):
                            with engine.connect() as connection:
                                connection.execute(text("DELETE FROM Votes WHERE (pollid = :pollid AND Userid = :userid)"), {'pollid': pollId, 'userid': current_user.id})
                                connection.commit()
                        new = Votes(
                            Counter = addCounter(engine),
                            Userid = current_user.id,
                            pollid = pollId,
                            voteoption = "".join(["option", str(i+1)])
                        )
                        db.session.add(new)
                        db.session.commit()
                return redirect(url_for("pollDisplay", pollId = pollId))
    else:
        if request.method == "GET":
            return render_template("pollresults.html", pollData = pollData, tallies = tallying(engine, pollId))
        if request.method == "POST":
            if request.form.get("viewDetails") is not None:
                return redirect(url_for("pollmore", pollId = pollId))
        
@login_required
@app.route("/main/polls/<pollId>/more", methods = ["GET", "POST"])
def pollmore(pollId):
    if request.method == "GET":
        privacy = (getpoll(engine, pollId))[5]
        match privacy:
            case "Hide":
                mode = 1
            case "ShowHalf":
                mode = 2
            case "Show":
                mode = 3
        return render_template("polldetails.html", mode = mode, pollId = pollId, info = whovoted(engine, pollId))