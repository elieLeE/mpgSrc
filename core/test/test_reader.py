# coding=utf-8

import unittest
from model.data_base import DataBase
from core import data_reader
from core.defines import Position


class TestReader(unittest.TestCase):
    def testDataBaseFielReader(self):
        filePath = r"/home/lee/Bureau/mpg/data/liga/j18.csv"

        dataBase = DataBase("", 0)
        data_reader.MPGDataBaseCSVFileReader(filePath).read(dataBase)

        self.assertTrue(len(dataBase._teams) == 20)
        self.assertTrue(len(dataBase._players) == 560, len(dataBase._players))

        player1 = "Real Madrid_Courtois Thibaut"
        player1Data = dataBase._players.get(player1, None)
        self.assertTrue(player1Data is not None)
        self.assertTrue(player1Data.getPosition() == Position.GOAL.value)

        player2 = "Girona_Ramalho Jonás"
        player2Data = dataBase._players.get(player2, None)
        self.assertTrue(player2Data is not None)
        self.assertTrue(player2Data.getPosition() == Position.CENTRAL_DEFENDER.value)

        player3 = "Sevilla_Escudero Sergio"
        player3Data = dataBase._players.get(player3, None)
        self.assertTrue(player3Data is not None)
        self.assertTrue(player3Data.getOffPrize() == 11)
        self.assertTrue(player3Data.getTeam().getId() == "Sevilla")
        self.assertTrue(player3Data.getGoalNumber() == 0)
        self.assertTrue(player3Data.getEval() == 5.7)
        self.assertTrue(player3Data.getPosition() == Position.LATERAL_DEFENDER.value)
        self.assertTrue(player3Data.getPercentTit() == 47)

        player4 = "Alavés_Manu García"
        player4Data = dataBase._players.get(player4, None)
        self.assertTrue(player4Data is not None)
        self.assertTrue(player4Data.getPosition() == Position.MILIEU_DEFENSIVE.value)

        player5 = "Atlético_Koke"
        player5Data = dataBase._players.get(player5, None)
        self.assertTrue(player5Data is not None)
        self.assertTrue(player5Data.getOffPrize() == 20)
        self.assertTrue(player5Data.getTeam().getId() == "Atlético")
        self.assertTrue(player5Data.getGoalNumber() == 1)
        self.assertTrue(player5Data.getEval() == 5.2)
        self.assertTrue(player5Data.getPosition() == Position.MILIEU_OFFENSIVE.value)
        self.assertTrue(player5Data.getPercentTit() == 76)

        player6 = "Barcelona_Messi Lionel"
        player6Data = dataBase._players.get(player6, None)
        self.assertTrue(player6Data is not None)
        self.assertTrue(player6Data.getOffPrize() == 55)
        self.assertTrue(player6Data.getTeam().getId() == "Barcelona")
        self.assertTrue(player6Data.getGoalNumber() == 15)
        self.assertTrue(player6Data.getEval() == 7)
        self.assertTrue(player6Data.getPosition() == Position.STRIKER.value)
        self.assertTrue(player6Data.getPercentTit() == 82)

    def testDataBaseXMLFileReader(self):
        dataBase = DataBase("", 0)

        # filePath = r"/home/lee/Bureau/mpg/data/ligue1/j38.xml"
        filePath = r"/home/lee/Bureau/mpg/data/liga/j18.xml"
        data_reader.MPGDataBaseXMLFileReader(filePath).read(dataBase)

        self.assertTrue(len(dataBase._teams) == 20)
        self.assertTrue(len(dataBase._players) == 560, len(dataBase._players))

        player1 = "Real Madrid_Courtois Thibaut"
        player1Data = dataBase._players.get(player1, None)
        self.assertTrue(player1Data is not None)
        self.assertTrue(player1Data.getPosition() == Position.GOAL.value)

        player2 = "Girona_Ramalho Jonás"
        player2Data = dataBase._players.get(player2, None)
        self.assertTrue(player2Data is not None)
        self.assertTrue(player2Data.getPosition() == Position.CENTRAL_DEFENDER.value)

        player3 = "Sevilla_Escudero Sergio"
        player3Data = dataBase._players.get(player3, None)
        self.assertTrue(player3Data is not None)
        self.assertTrue(player3Data.getOffPrize() == 11)
        self.assertTrue(player3Data.getTeam().getId() == "Sevilla")
        self.assertTrue(player3Data.getGoalNumber() == 0)
        self.assertTrue(player3Data.getEval() == 5.7)
        self.assertTrue(player3Data.getPosition() == Position.LATERAL_DEFENDER.value)
        self.assertTrue(player3Data.getPercentTit() == 47)

        player4 = "Alavés_Manu García"
        player4Data = dataBase._players.get(player4, None)
        self.assertTrue(player4Data is not None)
        self.assertTrue(player4Data.getPosition() == Position.MILIEU_DEFENSIVE.value)

        player5 = "Atlético_Koke"
        player5Data = dataBase._players.get(player5, None)
        self.assertTrue(player5Data is not None)
        self.assertTrue(player5Data.getOffPrize() == 20)
        self.assertTrue(player5Data.getTeam().getId() == "Atlético")
        self.assertTrue(player5Data.getGoalNumber() == 1)
        self.assertTrue(player5Data.getEval() == 5.2)
        self.assertTrue(player5Data.getPosition() == Position.MILIEU_OFFENSIVE.value)
        self.assertTrue(player5Data.getPercentTit() == 76)

        player6 = "Barcelona_Messi Lionel"
        player6Data = dataBase._players.get(player6, None)
        self.assertTrue(player6Data is not None)
        self.assertTrue(player6Data.getOffPrize() == 55)
        self.assertTrue(player6Data.getTeam().getId() == "Barcelona")
        self.assertTrue(player6Data.getGoalNumber() == 15)
        self.assertTrue(player6Data.getEval() == 7)
        self.assertTrue(player6Data.getPosition() == Position.STRIKER.value)
        self.assertTrue(player6Data.getPercentTit() == 82)


if __name__ == "__main__":
    TestReader().testDataBaseXMLFileReader()
