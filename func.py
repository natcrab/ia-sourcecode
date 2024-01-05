import re
from sqlalchemy import text
from werkzeug.security import check_password_hash


def valid_email(email):
    return bool (re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", email))

def duped_username(engine, username):
    with engine.connect() as connection:
        checkduplicates = connection.execute(text("SELECT username FROM users WHERE username = :username LIMIT 1"), {'username': username})
    for row in checkduplicates:   
        if (username == row.username):
            return True
    return False

def valid_username(username):
    if (len(username) > 20):
        return False
    if re.search(r"\s", username):
        return False
    if re.search(r"\W", username):
        return False
    return True

def valid_password(password):
    if (len(password) < 8 and len(password) > 0):
        return False
    #if bool(re.search(r"A-Z", password))== False:
       # return False
    #if bool(re.search(r"\W", password)) == False:
       # return False
    return True

def get_password(engine, username, password):
    with engine.connect() as connection:
        checkpass = connection.execute(text("SELECT password FROM users WHERE username = :username LIMIT 1"), {'username': username})
    for row in checkpass:
        return (check_password_hash(row.password, password))
        
def duped_pollId(engine, pollId):
    with engine.connect() as connection:
        checkduplicates = connection.execute(text("SELECT pollId FROM polls WHERE pollId = :pollId LIMIT 1"), {'pollId': pollId})
    for row in checkduplicates:   
        if (pollId == row.pollId):
            return True
    return False

def optioncountarr(optioncount):
    optioncountarray = []
    for i in range(optioncount):
        optioncountarray.append(i+1)
    return optioncountarray
    
def checkopts():
    return "placeholder"