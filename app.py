#importing various libraries and framework common to Flask
import os
import sys
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
    pollpopularity,
    gettime
)
from secretkey import keysec
from datetime import datetime, timedelta
from time import strftime
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
path = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'voters.db')
db = SQLAlchemy()
migrate = Migrate()
manage = LoginManager()
def creation():
    app = Flask(__name__)            
    app.config['SQLALCHEMY_DATABASE_URI'] = path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = keysec
    manage.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app
 
app = creation()
engine = create_engine(path)

#end initializing application

#initializing login manager



#Following the functionality of Flask-login library
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(256))
#Stored users data
    
#Polls Data
class Polls(db.Model):
    pollId = db.Column(db.String, primary_key=True, unique = True)
    creator = db.Column(db.String(20))
    pollname = db.Column(db.String)
    pollDescription = db.Column(db.String)
    pollQuestion = db.Column(db.String) #index 4
    privacyMode = db.Column(db.String)
    votingMode = db.Column(db.String)
    pollStart = db.Column(db.DateTime)
    publicity = db.Column(db.Boolean)
    pollTime = db.Column(db.DateTime) #index 9
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
    minscore = db.Column(db.Integer) #index 36
    maxscore = db.Column(db.Integer)
#End polls data

#Counting votes for users (popularity and score)
class Votes(db.Model):
    Counter = db.Column(db.Integer, primary_key = True, unique = True)
    Userid = db.Column(db.Integer)
    pollid = db.Column(db.String)
    voteoption = db.Column(db.String)
    score = db.Column(db.Integer)
    
#Counting votes for tideman
class Tideman(db.Model):
    Counter = db.Column(db.Integer, primary_key = True, unique = True)
    Userid = db.Column(db.Integer)
    pollid = db.Column(db.String)
    rank1 = db.Column(db.String)  #index 3
    rank2 = db.Column(db.String)
    rank3 = db.Column(db.String)
    rank4 = db.Column(db.String)
    rank5 = db.Column(db.String)
    rank6 = db.Column(db.String)
    rank7 = db.Column(db.String)
    rank8 = db.Column(db.String)
    rank9 = db.Column(db.String)
    rank10 = db.Column(db.String)
#End of vote counting

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

#Starting up the webpage
@app.route("/", methods = ["GET", "POST"])
def startup():
    if request.method == "GET":
        return redirect("/home")
    else:
        return "Oops, you aren't supposed to be here. It seems something had gone wrong"

#base webpage
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
            email = "no email" #standardized empty input
        #Check for valid input
        
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
        
        #User data into database if input is valid
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

#Content page 
@login_required
@app.route("/main", methods = ["GET", "POST"])
def contentpage():
    if request.method == "GET":
        if current_user.username is not None:
            user = current_user.username
        else:
            user = ""
        return render_template("content.html", user = user)
    elif request.method == "POST":
        if request.form.get("make") is not None:
            return redirect("/main/makepoll") #create poll page
        elif request.form.get("search") is not None:
            return redirect("/main/searchpoll") #find poll page
        elif request.form.get("logout") is not None:
            logout_user()
            return redirect("/home")
        elif request.form.get("Return") is not None:
            return redirect("/main") #Go to content page
    
@app.route("/main/makepoll", methods = ["GET", "POST"])
@login_required
def makepoll():
    if request.method == "GET":
        return render_template("pollinit.html")
    if request.method == "POST":
        if request.form.get("makepoll") is not None:
            optioncount = int(request.form.get("optionsnum")) #num of poll options
            needPass = int(request.form.get("passwordReq")) #whether the poll need a password
            if optioncount > 10 or optioncount<2:
                flash("Please enter a number between two and ten")
                return render_template("pollinit.html")
            else:
                return render_template("makepoll.html", optioncount = optioncountarr(optioncount), numopt = optioncount, needPass = needPass)
        elif request.form.get("create") is not None:
            #Name of inputs
            optionsarr = ["option1", "option2", "option3", "option4", "option5", "option6","option7","option8","option9","option10"] 
            explainsarr = ["explain1", "explain2","explain3","explain4","explain5","explain6","explain7","explain8","explain9","explain10",]
            pollOptions = []
            pollExplains = []
            optioncount = int(request.form.get("optcount"))
            needPass = int(request.form.get("passwordNeeded"))
           
            for i in range(optioncount): #Get the inputs of poll data using a loop               
                temp = request.form.get(optionsarr[i])
                if temp in pollOptions or temp == "":
                    flash("The poll options cannot be repeated or be empty")
                    return render_template("makepoll.html", optioncount = optioncountarr(optioncount), numopt = optioncount, needPass = needPass)
                pollOptions.append(temp)
                temp = request.form.get(explainsarr[i])
                pollExplains.append(temp)

            while len(pollOptions) < 10:  #Make sure index is in range
                pollOptions.append("")
                pollExplains.append("")
            pollId = str(request.form.get("pollId"))
            pollId = pollId.lower()      
            if duped_pollId(engine, pollId): #Ensure pollid is unique
                flash("poll Id already used, please pick another one")
                return render_template("makepoll.html", optioncount = optioncountarr(optioncount), numopt = optioncount, needPass = needPass)
            else: #Convert timer to seconds
                timerSeconds = int(request.form.get("timerDay"))*86400+int(request.form.get("timerHours"))*3600+int(request.form.get("timerMinutes"))*60+int(request.form.get("timerSeconds"))     
                
                #Standardizing the booleans
                if (request.form.get("pollPublicity")) == "1":
                    isPublic = True
                else:
                    isPublic = False
                if timerSeconds > 0:
                    manuality = False
                    pollTime = datetime.utcnow() + timedelta(seconds = timerSeconds)
                else:
                    manuality = True
                    pollTime = datetime.utcnow()
                if needPass == 1:
                    needPassBool = True
                    password = str(request.form.get("pollPassword"))
                    password = generate_password_hash(password)
                else:
                    needPassBool = False
                    password = ""
                minscore = request.form.get("minscore")
                maxscore = request.form.get("maxscore")
                if maxscore <= minscore:
                    minscore = 0
                
                #Input poll data into database
                new = Polls(
                    pollId = pollId,
                    creator = current_user.username,
                    pollname = request.form.get("pollName"),
                    pollDescription = request.form.get("pollDesc"),
                    pollQuestion = request.form.get("pollQuestion"),
                    privacyMode = request.form.get("pollPrivacy"),
                    votingMode = request.form.get("voteSystem"),
                    publicity = isPublic,
                    pollStart = datetime.utcnow(),
                    pollTime = pollTime,
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
                    option10exp = pollExplains[9],
                    minscore = minscore,
                    maxscore = maxscore,
                )
                db.session.add(new)
                db.session.commit()
                flash("Poll added to database!")
                return redirect("/main")
            
@app.route("/main/searchpoll/", methods = ["GET", "POST"]) 
@login_required 
def searchpoll():
    if request.method == "GET":
        mypolls = []
        with engine.connect() as connection:
            Mpolls = connection.execute(text("SELECT pollId from polls where creator = :username ORDER BY pollStart DESC LIMIT 100"), {'username': current_user.username})
        for i in Mpolls:
            mypolls.append(getpoll(engine, i.pollId))
        return render_template("searchpoll.html", toDisplay = mypolls)
    if request.method == "POST":
        if request.form.get("pollIdButton") is not None: #Search for polls using id
            if not duped_pollId(engine, request.form.get("searchPollId")):
                flash("No such poll ID!")
                return render_template("searchpoll.html")
            else:
                result = request.form.get("searchPollId")
                return redirect(url_for("pollDisplay", pollId = result))
        if request.form.get("pollNameButton") is not None:
            return redirect("/main/polls")
        numofPolls = int(request.form.get("numDisplay"))
        for i in range(numofPolls):
            if request.form.get("".join(["visitPoll", str(i+1)])) is not None: #visit the poll clicked on
                pollId = request.form.get("".join(["visitPollId", str(i+1)]))
                return redirect(url_for("pollDisplay", pollId = pollId))

@app.route("/main/polls", methods = ["GET", "POST"])
@login_required
def searchresults():
    if request.method == "GET":
        results = searchres(engine, "")
        toDisplay = []
        for i in results:
            toDisplay.append(getpoll(engine, i)) #Get all polls to be displayed by default
            n = len(toDisplay)
            for i in range(math.floor(n/2)): #Sort all polls from newest first by defaukt
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
                #Check which checkbox is ticked (find only finished or only ongoing polls)
                if "ongoing" not in x:   
                    for i in range(len(toDisplay)):
                        if toDisplay[i][15] == True:
                            toDisplay[i] = "rm"
                if "ended" not in x:   
                    for i in range(len(toDisplay)):
                        if toDisplay[i][15] == False:
                            toDisplay[i] = "rm" 
            except(IndexError):
                #If neither checkbox is checked, it would return an error (for some reason i don't really know)
                #Since no polls would be shown if neither checkbox is ticked anyways, I should just reset the page
                return redirect("/main/polls")
            finally:  
                while "rm" in toDisplay:
                    toDisplay.remove("rm")     #Remove all polls of the checkbox not ticked
                sortmode = request.form.get("searchSort") 

                #Rearrange the polls based on sorting mode
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
                            swapped = False
                            for k in range(0, length - i - 1, 1):
                                if pollpopularity(engine, toDisplay[k][0], toDisplay[k][6]) < pollpopularity(engine, toDisplay[k+1][0], toDisplay[k+1][6]):
                                    temp = toDisplay[k] 
                                    toDisplay[k] = toDisplay[k+1]
                                    toDisplay[k+1] = temp
                                    swapped = True
                            if swapped == False:
                                break
                    case _:
                        pass                
                return render_template("pollfind.html", toDisplay = toDisplay)
        else:
            numofPolls = int(request.form.get("numofDisplay"))
            for i in range(numofPolls):
                if request.form.get("".join(["visitPoll", str(i+1)])) is not None: #visit the poll clicked on
                    pollId = request.form.get("".join(["visitPollId", str(i+1)]))
                    return redirect(url_for("pollDisplay", pollId = pollId)) 



@app.route("/main/polls/<pollId>", methods = ["GET", "POST"])
@login_required
def pollDisplay(pollId):
    pollData = getpoll(engine, pollId)
    passEntered = False
    if current_user.username == pollData[1]: #Automatically let user in if they created the poll without password prompt
        isOwner = True
        passEntered = True
    else:
        isOwner = False
    remains = datetime.strptime(gettime(engine, pollId), '%Y-%m-%d %H:%M:%S.%f') - datetime.utcnow() #Time remaining
    if (not pollData[10]) and pollData[15]:
        if remains.total_seconds() < 0.0: #Ends poll automatically if timer runs out
            with engine.connect() as connection: 
            #Note: Always do this instead of using engine.connect().execute() because
            #it will automatically creates and then close an instance of database cursor without additional work
                connection.execute(text("UPDATE Polls Set ongoing = False WHERE pollid = :pollid"), {'pollid': pollId})
                connection.commit()
            pollData[15] = False
    if pollData[15]: #Voting ongoing
        if request.method == "GET":
            return render_template("polldata.html", pollData = pollData, voted = checkvoted(engine, current_user.id, pollId, pollData[6]), optvoted = "".join(list(optvoted(engine, current_user.id, pollId))[6:]), isOwner = isOwner, passEntered = passEntered, Remains = str(remains)[:-7])           
        if request.method == "POST":
            if request.form.get("pollPassButton") is not None:
                password = request.form.get("pollPass")
                if pollpassword(engine, pollId, password):                   
                    return render_template("polldata.html", pollData = pollData, voted = checkvoted(engine, current_user.id, pollId, pollData[6]), optvoted = "".join(list(optvoted(engine, current_user.id, pollId))[6:]), isOwner = isOwner, passEntered= True, Remains = str(remains)[:-7])
                else:
                    flash("Wrong password, please try again")
                    return redirect(url_for("pollDisplay", pollId = pollId))
            if request.form.get("endpoll") is not None:
                with engine.connect() as connection: #Let creator end the poll
                    connection.execute(text("UPDATE Polls Set ongoing = False WHERE pollid = :pollid"), {'pollid': pollId})
                    connection.execute(text("UPDATE Polls Set pollTime = :datetime WHERE pollid = :pollid"), {'pollid': pollId, 'datetime': datetime.utcnow()})
                    connection.commit()
                redirect(url_for("pollDisplay", pollId = pollId))
            if request.form.get("changepass") is not None: #Let creator change the password of the poll
                password = str(request.form.get("pollPassNew"))
                password = generate_password_hash(password)
                with engine.connect() as connection:
                    connection.execute(text("UPDATE Polls Set password = :password WHERE pollid = :pollid"), {'pollid': pollId, 'password': password})
                    connection.commit()
                flash("Password change success!")
                redirect(url_for("pollDisplay", pollId = pollId))

           
            if pollData[6] == "popularity":
                for i in range(pollData[12]):
                    if request.form.get("".join(["option", str(i+1)])) is not None:
                        if checkvoted(engine, current_user.id, pollId, "popularity"):
                            with engine.connect() as connection: #Change votes
                                connection.execute(text("DELETE FROM Votes WHERE (pollid = :pollid AND Userid = :userid)"), {'pollid': pollId, 'userid': current_user.id})
                                connection.commit()
                        new = Votes( #Add votes to database
                            Counter = addCounter(engine, "Votes"),
                            Userid = current_user.id,
                            pollid = pollId,
                            voteoption = "".join(["option", str(i+1)]),
                            score = 0
                        )
                        db.session.add(new)
                        db.session.commit()
            
            
            elif pollData[6] == "score":
                if request.form.get("submitScore") is not None:
                    if checkvoted(engine, current_user.id, pollId, "score"):
                        with engine.connect() as connection: #Change votes
                            connection.execute(text("DELETE FROM Votes WHERE (pollid = :pollid AND Userid = :userid)"), {'pollid': pollId, 'userid': current_user.id})
                            connection.commit()
                    for i in range(pollData[12]):
                        new = Votes( #Add votes to database
                            Counter = addCounter(engine, "Votes"),
                            Userid = current_user.id,
                            pollid = pollId,
                            voteoption = "".join(["option", str(i+1)]),
                            score = request.form.get("".join(["score", str(i+1)]))
                        )
                        db.session.add(new)
                        db.session.commit()
            
            
            elif pollData[6] == "tideman":
                if request.form.get("submitTideman") is not None:
                    if checkvoted(engine, current_user.id, pollId, "tideman"):
                        with engine.connect() as connection: #Change votes
                            connection.execute(text("DELETE FROM Tideman WHERE (pollid = :pollid AND Userid = :userid)"), {'pollid': pollId, 'userid': current_user.id})
                            connection.commit() 
                    #Processing the votes
                    rank = [] 
                    result = []   
                    for i in range(pollData[12]):
                        temp = int(request.form.get("".join(["tideman", str(i+1)])))
                        if temp in rank:
                            flash("Each option must have a unique ranking")
                            return redirect(url_for("pollDisplay", pollId = pollId))
                        rank.append(temp)                   
                    for i in range(pollData[12]):
                        result.append(rank.index(i+1)+1)
                    while(len(result)< 10):
                        result.append(0)
                    
                    new = Tideman( #Add votes to database
                        Counter = addCounter(engine, "Tideman"),
                        Userid = current_user.id,
                        pollid = pollId,
                        rank1 = "".join(["option", str(result[0])]),
                        rank2 = "".join(["option", str(result[1])]),
                        rank3 = "".join(["option", str(result[2])]),
                        rank4 = "".join(["option", str(result[3])]),
                        rank5 = "".join(["option", str(result[4])]),
                        rank6 = "".join(["option", str(result[5])]),
                        rank7 = "".join(["option", str(result[6])]),
                        rank8 = "".join(["option", str(result[7])]),
                        rank9 = "".join(["option", str(result[8])]),
                        rank10 = "".join(["option", str(result[9])]),
                    )
                    db.session.add(new)
                    db.session.commit()                 
            else: 
                flash("Oops! It seems something went wrong with the poll!")
                return redirect("/main/searchpoll") #Prevent weird interaction with timer
            flash("Your vote has been submitted")
            return redirect(url_for("pollDisplay", pollId = pollId))
    else: #Voting ended
        if request.method == "GET": #Show poll results 
            return render_template("pollresults.html", pollData = pollData, tallies = tallying(engine, pollId, pollData[6]))
        if request.method == "POST":
            if request.form.get("viewDetails") is not None:
                return redirect(url_for("pollmore", pollId = pollId))
        

@app.route("/main/polls/<pollId>/more", methods = ["GET", "POST"]) #poll details
@login_required
def pollmore(pollId):
    with engine.connect() as connection:
        connect = connection.execute(text("SELECT * FROM Polls WHERE pollid = :pollid"), {'pollid': pollId}).fetchone()
    votetype = connect.votingMode
    num = connect.NumofOptions
    if request.method == "GET":
        privacy = (getpoll(engine, pollId))[5]
        match privacy:
            case "Hide":
                mode = 1 #No voters shown
            case "ShowHalf":
                mode = 2 #Show voters only
            case "Show":
                mode = 3 #Show voters and their votes
        with engine.connect() as connection:
            time = connection.execute(text("SELECT pollStart from Polls where pollid = :pollid"), {'pollid': pollId}).fetchone()
        start = datetime.strptime(time.pollStart, '%Y-%m-%d %H:%M:%S.%f')
        ended = datetime.strptime(gettime(engine, pollId), '%Y-%m-%d %H:%M:%S.%f')
        ongoing  =  ended - start
        info =  whovoted(engine, pollId, votetype)
        placeholder = []
        scores = []
        if votetype == "score":
            for i in info:
                with engine.connect() as connection:
                    username = connection.execute(text("SELECT id from Users WHERE username = :username"), {'username': i}).fetchone()
                placeholder.append(username.id)
            for i in placeholder:
                with engine.connect() as connection:
                    temp = connection.execute(text("SELECT score from Votes WHERE pollid = :pollid AND Userid = :Userid"), {'pollid': pollId, 'Userid': i})
                pholder = []
                for row in temp:  
                    pholder.append(row.score)
                scores.append(pholder)
            print(scores)
        return render_template("polldetails.html", mode = mode, pollId = pollId, info = info, start = str(start)[:-7], ended = str(ended)[:-7], ongoing = str(ongoing)[:-7], votetype = votetype, scores = scores, num = num)
    if request.method == "POST":
        if request.form.get("back") is not None:
            return redirect(url_for("pollDisplay", pollId = pollId))
