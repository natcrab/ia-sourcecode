import re
from sqlalchemy import text
from werkzeug.security import check_password_hash


def valid_email(email):
    return bool (re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", email))

def duped_username(engine, username):
    userN = username.lower()
    with engine.connect() as connection:
        checkduplicates = connection.execute(text("SELECT username FROM users WHERE LOWER(username) = :username LIMIT 1"), {'username': userN})
    for row in checkduplicates:
        if (userN == row.username.lower()):
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
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[@$!%*#?&]", password):
        return False
    return True

def get_password(engine, username, password):
    userN = username.lower()
    with engine.connect() as connection:
        checkpass = connection.execute(text("SELECT password FROM users WHERE LOWER(username) = :username LIMIT 1"), {'username': userN})
    for row in checkpass:
        return (check_password_hash(row.password, password))
        
def duped_pollId(engine, pollId):
    ID = pollId.lower()
    with engine.connect() as connection:
        checkduplicates = connection.execute(text("SELECT pollId FROM polls WHERE LOWER(pollId) = :pollId LIMIT 1"), {'pollId': ID})
    for row in checkduplicates:   
        if (ID == row.pollId.lower()):
            return True
    return False

def optioncountarr(optioncount):
    optioncountarray = []
    for i in range(optioncount):
        optioncountarray.append(i+1)
    return optioncountarray
    

def getUsername(engine, username):
    userN = username.lower()
    with engine.connect() as connection:
        checkduplicates = connection.execute(text("SELECT username FROM users WHERE LOWER(username) = :username LIMIT 1"), {'username': userN})
        for row in checkduplicates:
            returnString = "".join(row)
        return returnString


    
    


