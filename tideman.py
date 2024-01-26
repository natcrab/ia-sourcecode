def tideman(options, votes):
    preferences = []
    lock = []
    pairs = []
    paircount = 0
    votercount = len(votes)
    Num = len(options)
    for i in range(Num):
        preferences.append([])
        lock.append([])
        for k in range(Num):
            preferences[i].append(0)
            lock[i].append(False)
    for i in range(votercount):
        onevote = []
        for k in range(Num):
            onevote.append(int((list(votes[i][k+3]))[6])-1)
        for k in range(Num):
            for j in range(k, Num, 1):
                preferences[onevote[k]][onevote[j]] +=1
    for i in range(Num):
        for k in range(Num):
            if(preferences[i][k] > preferences [k][i]):
                pairs.append([])
                pairs[paircount].append(i)
                pairs[paircount].append(k)
                paircount += 1
    for i in range(paircount):
        for k in range(i+1, paircount, 1):
            if (preferences[pairs[i][0]][pairs[i][1]] < preferences[pairs[k][0]][pairs[k][1]]):
                temp = [pairs[i][0], pairs[i][1]]
                pairs[i][0] = pairs[k][0]
                pairs[i][1] = pairs[k][1]
                pairs[k][0] = temp[0]
                pairs[k][1] = temp[1]
    for i in range(paircount):
        if (not graph_create(lock, Num, pairs[i][0],  pairs[i][1])):
            lock[pairs[i][0]][pairs[i][1]] = True
    winners = []
    for i in range(Num):
        winners.append(True)
    for i in range(Num):
        for k in range(Num):
            if lock[k][i]:
                winners[i] = False
    results = []
    for i in range(Num):
        if winners[i]:
            results.append(i+1)
    return results


def graph_create(lock, Num, i, k):
    if lock[k][i]  == True:
        return True
    for j in range(0, Num, 1):
        if lock[k][j]:
            if graph_create(lock, Num, i, j):
                return True
    return False

