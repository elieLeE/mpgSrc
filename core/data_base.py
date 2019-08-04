# coding=utf-8


class DataBase(object):
    def __init__(self, champName, dayNumber):
        self._champName = champName
        self._dayNumber = dayNumber

        self._players = {}
        self._teams = {}

    def getChampName(self):
        return self._champName

    def getDayNumber(self):
        return self._dayNumber

    def getAllTeams(self):
        return self._teams.values()

    def addPlayer(self, playerInst):
        self._players[playerInst.getId()] = playerInst

    def getPlayer(self, idPlayer):
        return self._players.get(idPlayer, None)

    def addTeam(self, teamInst):
        self._teams[teamInst.getId()] = teamInst

