# coding=utf-8


class Player(object):
    def __init__(self, _id, name, position, eval, goalNumber, prize, percentTit, teamInst=None):
        self._id = _id
        self._name = name
        self._position = position
        self._eval = eval
        self._goalNumber = goalNumber
        self._prize = prize
        self._percentTit = percentTit

        self._teamInst = None
        if teamInst is not None:
            self.setTeam(teamInst)

    def getId(self):
        return self._id

    def getName(self):
        return self._name

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
