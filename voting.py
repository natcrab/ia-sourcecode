from sqlalchemy import text
from werkzeug.security import check_password_hash
from tideman import tideman

def getpoll(engine, pollId):   
    ID = pollId.lower()
    with engine.connect() as connection:
        getDetails = connection.execute(text("SELECT * FROM polls WHERE LOWER(pollId) = :pollId LIMIT 1"), {'pollId': ID}).fetchone()
        details = list(getDetails)
        return details
    

def checkvoted(engine, userid, pollid, polltype):
    with engine.connect() as connection:
        if polltype == "score" or polltype == "popularity":
            checkduplicates = connection.execute(text("SELECT Userid FROM Votes WHERE pollid = :pollid"), {'pollid': pollid})
        elif polltype == "tideman":
            checkduplicates = connection.execute(text("SELECT Userid FROM Tideman WHERE pollid = :pollid"), {'pollid': pollid})
    for row in checkduplicates:
        if (userid == row.Userid):
            return 1
    return 0

def optvoted(engine, userid, pollid):
    with engine.connect() as connection:
        getOptVoted = connection.execute(text("SELECT voteoption FROM Votes WHERE (pollid = :pollid AND Userid = :userid) LIMIT 1"), {'pollid': pollid, 'userid': userid}).fetchone()
        if getOptVoted is not None: 
            getOptVoted = list(getOptVoted)
            return getOptVoted[0]
        else:
            return "option-1"
    
def tallying(engine, pollid, polltype):
    if polltype == "tideman":
        votes = []
        options = []
        pollinfo = getpoll(engine, pollid)
        n = 0
        for i in range(16, 36, 2):
            if (n < pollinfo[12]):
                options.append(pollinfo[i])
                n+=1
            else:
                break
        with engine.connect() as connection:
            temp = connection.execute(text("SELECT * from Tideman WHERE pollid = :pollid"), {'pollid': pollid})
        for row in temp:
            votes.append(list(row))
        arr = tideman(options, votes)
        for i in range(len(arr)):
            arr[i] = "".join(["option ", str(arr[i])])
        return arr       
    else:
        with engine.connect() as connection:
            results = []
            optCount = connection.execute(text("SELECT NumofOptions FROM Polls WHERE pollId = :pollid LIMIT 1"), {'pollid': pollid}).fetchone()
            optCount = (list(optCount))[0]
            for i in range(optCount):
                option = "".join(["option", str(i+1)])
                if polltype == "popularity":
                    temp = connection.execute(text("SELECT COUNT (*) From Votes WHERE (voteoption = :option AND pollid = :pollid)"), {'option': option, 'pollid': pollid}).fetchone()
                elif polltype == "score":
                    temp = connection.execute(text("SELECT SUM(score) From Votes WHERE (voteoption = :option AND pollid = :pollid)"), {'option': option, 'pollid': pollid}).fetchone()                   
                results.append((list(temp))[0])
        x = len(results)
        print(x)
        for i in range(x):
            if results[i] == max(results[0:x]):
                results.append(i)
        return results

def whovoted(engine, pollid, polltype):
    if polltype == "tideman":
        results = []
        x = 0
        with engine.connect() as connection:
            people = connection.execute(text("SELECT * from Tideman WHERE pollid = :pollid"), {'pollid': pollid})
            for row in people:
                results.append(list(row))
                username = connection.execute(text("SELECT username from Users WHERE id = :id"), {'id': row.Userid}).fetchone()
                results[x][1] = (list(username))[0]
                x+=1
            return results
    else:
        results = []
        with engine.connect() as connection:
            people = connection.execute(text("SELECT * from Votes WHERE pollid = :pollid"), {'pollid': pollid})
            x = 0
            for row in people:
                results.append(list(row))
                username = connection.execute(text("SELECT username from Users WHERE id = :id"), {'id': row.Userid}).fetchone()
                results[x][1] = (list(username))[0]
                x+=1
            if polltype == "popularity":                 
                return results
            elif polltype == "score":
                arr = []
                for i in range(len(results)):
                    if results[i][1] not in arr:
                        arr.append(results[i][1])
                return arr
            

def addCounter(engine, polltype):
    with engine.connect() as connection:
        if (polltype == "Votes"):
            Counter = connection.execute(text("SELECT MAX (Counter) FROM Votes")).fetchone()
        elif (polltype == "Tideman"):
            Counter = connection.execute(text("SELECT MAX (Counter) FROM Tideman")).fetchone()
    if (list(Counter))[0] is not None:
        return int((list(Counter))[0])+ 1
    else:
        return 1
    
def searchres(engine, keyword):   
    result = []
    with engine.connect() as connection:
        getDetails = connection.execute(text("SELECT pollId FROM polls WHERE (LOWER(pollname) LIKE :keyword OR LOWER(pollDescription) LIKE :keyword OR LOWER(pollQuestion) ORDER BY pollStart LIKE :keyword) LIMIT 50"), {'keyword': "%" + keyword.lower() + "%"})
        for row in getDetails:
            result.append(row.pollId)
        return result
    
def pollpassword(engine, pollid, password):
    with engine.connect() as connection:
        checkpass = connection.execute(text("SELECT password FROM Polls WHERE pollId = :pollid LIMIT 1"), {'pollid': pollid})
    for row in checkpass:
        return (check_password_hash(row.password, password))
    
def pollpopularity(engine, pollid, votesystem):
    if votesystem == "tideman":
        with engine.connect() as connection:
            num = connection.execute(text("SELECT COUNT (DISTINCT Userid) From Tideman WHERE pollid = :pollid"), {'pollid': pollid}).fetchone() 
    else:
        with engine.connect() as connection:
            num = connection.execute(text("SELECT COUNT (DISTINCT Userid) From Votes WHERE pollid = :pollid"), {'pollid': pollid}).fetchone()
    return num

def gettime(engine, pollid):
    with engine.connect() as connection:
        time = connection.execute(text("SELECT pollTime from Polls where pollid = :pollid"), {'pollid': pollid}).fetchone()
        end = time.pollTime
    return end
