# coding=utf-8

from core.defines import Position


class Team(object):
    def __init__(self, _id):
        self._id = _id
        self._players = {Position.GOAL.value: [], Position.DEFENDER.value: [], Position.MILIEU.value: [], Position.STRIKER.value: []}

    def getId(self):
        return self._id

    def addPlayer(self, playerInst):
        self._players[Position.getGloBasPos(playerInst.getPosition())].append(playerInst)

    def getAllPlayers(self):
        l = []
        for playersList in self._players.values():
            l.extend(playersList)
        return l
