# coding=utf-8

from PySide2 import QtWidgets
from gui import widgets
from gui.defines import LayoutType
from gui.league_widget import LeagueWidget


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        self._tabWidget = None

        self.setupUi()

    def setupUi(self):
        mainLayout = widgets.getConfiguredLayout(LayoutType.VERTICAL.value, parent=self)
        self._tabWidget = QtWidgets.QTabWidget(self)
        mainLayout.addWidget(self._tabWidget)

    def addNewTabLeague(self, leagueInst, applicationManager):
        self._tabWidget.addTab(LeagueWidget(leagueInst, applicationManager, self), leagueInst.getName())
