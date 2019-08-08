# coding=utf-8

from PySide2 import QtWidgets
from gui.mercato_widget import MercatoWidget
from gui.league_info_widget import LeagueInfoWidget


class LeagueWidget(QtWidgets.QWidget):
    def __init__(self, leagueItem, parent):
        super(LeagueWidget, self).__init__(parent)
        self._leagueItem = leagueItem

        self._label = None
        self._mercatoWidget = None
        self._leagueInfoWidget = None

        self.setupUi()

    def setupUi(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        toolbar = QtWidgets.QToolBar(self.tr("Tool bar"), self)
        toolbar.setMovable(False)

        mainLayout.addWidget(toolbar)

        tabWidget = QtWidgets.QTabWidget(self)
        self._mercatoWidget = MercatoWidget(self._leagueItem, self)
        tabWidget.addTab(self._mercatoWidget, "Mercato")

        self._leagueInfoWidget = LeagueInfoWidget(self._leagueItem, self)
        tabWidget.addTab(self._leagueInfoWidget, "League info")

        mainLayout.addWidget(tabWidget)