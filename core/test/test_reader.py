# coding=utf-8

import unittest
from core.data_base import DataBase
from core import data_reader
from core.defines import Position


class TestReader(unittest.TestCase):
    def testDataBaseFielReader(self):
        filePath = r"/home/lee/Bureau/mpg/data/liga/j18.csv"

        dataBase = DataBase()
        data_reader.MPGDataBaseFileReader(filePath).read(dataBase)

        self.assertTrue(len(dataBase._teams) == 20)
        self.assertTrue(len(dataBase._players) == 555)

        player1 = "Courtois Thibaut"
        player1Data = dataBase._players.get(player1, None)
        self.assertTrue(player1Data is not None)
        self.assertTrue(player1Data.getPosition() == Position.GOAL.value)

        player2 = "Ramalho Jonás"
        player2Data = dataBase._players.get(player2, None)
        self.assertTrue(player2Data is not None)
        self.assertTrue(player2Data.getPosition() == Position.DEF_CENTRAL.value)

        player3 = "Escudero Sergio"
        player3Data = dataBase._players.get(player3, None)
        self.assertTrue(player3Data is not None)
        self.assertTrue(player3Data.getPrize() == 11)
        self.assertTrue(player3Data.getTeam().getId() == "Sevilla")
        self.assertTrue(player3Data.getGoalNumber() == 0)
        self.assertTrue(player3Data.getEval() == 5.7)
        self.assertTrue(player3Data.getPosition() == Position.DEF_LATERAL.value)
        self.assertTrue(player3Data.getPercentTit() == 47)

        player4 = "Manu García"
        player4Data = dataBase._players.get(player4, None)
        self.assertTrue(player4Data is not None)
        self.assertTrue(player4Data.getPosition() == Position.MILIEU_DEFENSIF.value)

        player5 = "Koke"
        player5Data = dataBase._players.get(player5, None)
        self.assertTrue(player5Data is not None)
        self.assertTrue(player5Data.getPrize() == 20)
        self.assertTrue(player5Data.getTeam().getId() == "Atlético")
        self.assertTrue(player5Data.getGoalNumber() == 1)
        self.assertTrue(player5Data.getEval() == 5.2)
        self.assertTrue(player5Data.getPosition() == Position.MILIEU_OFFENSIF.value)
        self.assertTrue(player5Data.getPercentTit() == 76)

        player6 = "Messi Lionel"
        player6Data = dataBase._players.get(player6, None)
        self.assertTrue(player6Data is not None)
        self.assertTrue(player6Data.getPrize() == 55)
        self.assertTrue(player6Data.getTeam().getId() == "Barcelona")
        self.assertTrue(player6Data.getGoalNumber() == 15)
        self.assertTrue(player6Data.getEval() == 7)
        self.assertTrue(player6Data.getPosition() == Position.ATTAQUANT.value)
        self.assertTrue(player6Data.getPercentTit() == 82)


if __name__ == "__main__":
    TestReader().testDataBaseFielReader()
