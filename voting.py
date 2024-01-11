from sqlalchemy import text

def getpoll(engine, pollId):   
    ID = pollId.lower()
    with engine.connect() as connection:
        getDetails = connection.execute(text("SELECT * FROM polls WHERE LOWER(pollId) = :pollId LIMIT 1"), {'pollId': ID}).fetchone()
        details = list(getDetails)
        return details
    
def checkvoted(engine, userid, pollid):
    with engine.connect() as connection:
        checkduplicates = connection.execute(text("SELECT Userid FROM Votes WHERE pollid = :pollid"), {'pollid': pollid})
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
    
def tallying(engine, pollid):
    with engine.connect() as connection:
        results = []
        optCount = connection.execute(text("SELECT NumofOptions FROM Polls WHERE pollId = :pollid LIMIT 1"), {'pollid': pollid}).fetchone()
        optCount = (list(optCount))[0]
        for i in range(optCount):
            option = "".join(["option", str(i+1)])
            temp = connection.execute(text("SELECT COUNT (*) From Votes WHERE (voteoption = :option AND pollid = :pollid)"), {'option': option, 'pollid': pollid}).fetchone()
            results.append((list(temp))[0])
    x = len(results)
    for i in range(x):
        if results[i] == max(results[0:optCount-1]):
            results.append(i)
    return results

def addCounter(engine):
    with engine.connect() as connection:
        Counter = connection.execute(text("SELECT MAX (Counter) FROM Votes")).fetchone()
    if (list(Counter))[0] is not None:
        return int((list(Counter))[0])+ 1
    else:
        return 1
    
def searchres(engine, keyword):   
    keyW = keyword.lower()
    result = []
    with engine.connect() as connection:
        getDetails = connection.execute(text("SELECT pollId FROM polls WHERE (LOWER(pollname) LIKE :keyword OR LOWER(pollDescription) LIKE :keyword OR LOWER(pollQuestion) LIKE :keyword)"), {'keyword': "%" + keyword + "%"})
        for row in getDetails:
            result.append(row.pollId)
        return result