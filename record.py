from score import Score

def readranking():
    ranking = []
    with open('record.txt', 'r') as record:
        lines = record.readlines()
        for i, line in enumerate(lines):
            if i != 0:
                vect = line.rstrip('\n').split('\t')
                ranking.append(Score(*vect))
    return ranking

def getBestScore():
    ranking = readranking()
    best = max([el.points for el in ranking])
    return best

def getRanking():
    ranking = readranking()
    s = ''
    for el in ranking:
        for i in range(10):
            if el.rank == i+1:
                s += '{}\t{}\t{}\t{}\t{}\n'.format(el.rank, el.name, el.level, el.points, el.date)
    return s.rstrip('\n')
    
def checkRecord(level, points, date, name):
    playerScore = Score(0, '', level, points, date)
    if playerScore.isGood():
        playerScore.name = name
        newranking = playerScore.getNewRank()
        playerScore.saveRanking(newranking)
    return getRanking()

