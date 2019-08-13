# coding=utf-8


class Player(object):
    def __init__(self, _id, name, position, eval, goalNumber, officialPrize, buyPrize, percentTit, teamInst=None):
        self._id = _id
        self._name = name
        self._position = position
        self._eval = eval
        self._goalNumber = goalNumber
        self._offPrize = officialPrize
        self._buyPrize = buyPrize
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

    def getOffPrize(self):
        return self._offPrize

    def getBuyPrize(self):
        return self._buyPrize

    def getPercentTit(self):
        return self._percentTit

    def setTeam(self, teamInst):
        self._teamInst = teamInst
        teamInst.addPlayer(self)
