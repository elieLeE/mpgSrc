# coding=utf-8


class Team(object):
    def __init__(self, _id):
        self._id = _id
        self._players = {}

    def getId(self):
        return self._id

    def addPlayer(self, playerInst):
        self._players[playerInst.getId()] = playerInst

    def getAllPlayers(self):
        return self._players.values()
