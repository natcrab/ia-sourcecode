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
        getOptVoted = connection.execute(text("SELECT voteoption FROM Votes WHERE pollid = :pollid AND Userid = :userid LIMIT 1"), {'pollid': pollid, 'userid': userid}).fetchone()
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
            temp = connection.execute(text("SELECT COUNT (*) From Votes WHERE voteoption = :option"), {'option': option}).fetchone()
            results.append((list(temp))[0])
    for i in range(len(results)):
        if results[i] == max(results):
            results.append(i)
    return results

def addCounter(engine):
    with engine.connect() as connection:
        Counter = connection.execute(text("SELECT MAX (Counter) FROM Votes")).fetchone()
        return (list(Counter))[0]+ 1