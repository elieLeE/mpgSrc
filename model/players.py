class Player(object):
    def __init__(self, name, position, realTeamName, noteMoy, nbrGoals, price, percentageTit):
        self._name = name
        self._pos = position
        self._realTeamName = realTeamName
        self._noteMoy = noteMoy
        self._nbrGoals = nbrGoals
        self._price = price
        self._percentageTit = percentageTit

    def getName(self):
        return self._name

    def getPos(self):
        return self._pos

    def getRealTeamName(self):
        return self._realTeamName

    def getNoteMoy(self):
        return self._noteMoy

    def getNbrGoals(self):
        return self._nbrGoals

    def getPrice(self):
        return self._price

    def getPercentageTit(self):
        return self._percentageTit
