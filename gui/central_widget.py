# coding=utf-8

from PySide2 import QtWidgets
from gui.league_widget import LeagueWidget


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        self._tabWidget = None

        self.setupUi()

    def setupUi(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        self._tabWidget = QtWidgets.QTabWidget(self)

        mainLayout.addWidget(self._tabWidget)

    def addNewTabLeague(self, coreItem, applicationManager):
        self._tabWidget.addTab(LeagueWidget(coreItem, applicationManager, self), coreItem.getName())
