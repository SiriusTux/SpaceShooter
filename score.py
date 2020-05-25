import bisect
import os

class Score:

    def __init__(self, rank, name, level, points, date): 
        self.level = level
        self.points = int(points)
        self.date =  date
        self.rank = int(rank)
        self.name = name
        self.ranking_file = os.path.join('storage', 'record.txt')

    def getRanking(self):
        ranking = []
        with open(self.ranking_file, 'r') as record:
            lines = record.readlines()
            for i, line in enumerate(lines):
                if i != 0:
                    vect = line.rstrip('\n').split('\t')
                    ranking.append(Score(*vect))
        return ranking

    def isGood(self):
        actualRanking = self.getRanking()
        for element in actualRanking:
            if self.points >= element.points:
                return True
        return False

    def getNewRank(self):
        actualRanking = self.getRanking()
        best_scores = sorted([obj.points for obj in actualRanking])
        bisect.insort(best_scores, self.points)
        best_scores = sorted(list(set(best_scores)), reverse=True)
        newRanking = []
        for rank, score in enumerate(best_scores):
            players = [obj for obj in actualRanking if obj.points == score and self.points != score]
            if players:
                for i, player in enumerate(players):
                    player.rank = rank + i +1
                    newRanking.append(player)
                    if len(newRanking) == 10:
                        return newRanking
            else:
                self.rank = rank + 1
                newRanking.append(self)
        return newRanking


    def saveRanking(self, ranking):
        ranking_vect = sorted([ obj.rank for obj in ranking ])
        with open(self.ranking_file, 'w') as record:
            record.write('rank\tname\tlevel\tscore\tdate\n')
            for rank in ranking_vect:
                for element in ranking:
                    if element.rank == rank:
                        record.write('{}\t{}\t{}\t{}\t{}\n'.format(element.rank, element.name, element.level, element.points, element.date))
