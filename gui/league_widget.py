# coding=utf-8

from PySide2 import QtWidgets
from core import data_reader
from gui.mercato_widget import MercatoWidget
from gui.league_info_widget import LeagueInfoWidget


class LeagueWidget(QtWidgets.QWidget):
    def __init__(self, leagueItem, applicationManager, parent):
        super(LeagueWidget, self).__init__(parent)
        self._leagueItem = leagueItem
        self._applicationManager = applicationManager

        self._label = None
        self._mercatoWidget = None
        self._leagueInfoWidget = None

        self.setupUi()

    def setupUi(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        tabWidget = QtWidgets.QTabWidget(self)
        self._mercatoWidget = MercatoWidget(self._leagueItem, self)
        tabWidget.addTab(self._mercatoWidget, "Mercato")

        self._leagueInfoWidget = LeagueInfoWidget(self._leagueItem, self)
        tabWidget.addTab(self._leagueInfoWidget, "League info")

        mainLayout.addWidget(tabWidget)

    def loadNewDataBase(self):
        dataBaseInst = self._leagueItem.getDataBase()
        dataBaseInst.clear()
        data_reader.MPGDataBaseCSVFileReader(r"/home/lee/Bureau/mpg/data/liga/j18.csv").read(dataBaseInst)

