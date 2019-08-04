# coding=utf-8


class Player(object):
    def __init__(self, _id, position, eval, goalNumber, prize, percentTit):
        self.__id = _id
        self._position = position
        self._eval = eval
        self._goalNumber = goalNumber
        self._prize = prize
        self._percentTit = percentTit

        self._teamInst = None

    def getId(self):
        return self.__id

    def getPosition(self):
        return self._position

    def getTeam(self):
        return self._teamInst

    def getEval(self):
        return self._eval

    def getGoalNumber(self):
        return self._goalNumber

    def getPrize(self):
        return self._prize

    def getPercentTit(self):
        return self._percentTit

    def setTeam(self, teamInst):
        self._teamInst = teamInst
        teamInst.addPlayer(self)
