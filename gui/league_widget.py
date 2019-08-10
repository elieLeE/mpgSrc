# coding=utf-8

from PySide2 import QtWidgets
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
        self._chooseDataBase()

    def setupUi(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        toolbar = QtWidgets.QToolBar(self.tr("Tool bar"), self)
        toolbar.setStyleSheet("QToolBar {background-color: grey;}")
        toolbar.setMovable(False)

        chooseDataBase = toolbar.addAction("Choose data base")
        chooseDataBase.triggered.connect(self._chooseDataBase)

        mainLayout.addWidget(toolbar)

        tabWidget = QtWidgets.QTabWidget(self)
        self._mercatoWidget = MercatoWidget(self._leagueItem, self)
        tabWidget.addTab(self._mercatoWidget, "Mercato")

        self._leagueInfoWidget = LeagueInfoWidget(self._leagueItem, self)
        tabWidget.addTab(self._leagueInfoWidget, "League info")

        mainLayout.addWidget(tabWidget)

    def _chooseDataBase(self):
        actualDataBase = self._leagueItem.getDataBase()
        self._applicationManager.loadDataBaseInLeague(self._leagueItem, r"/home/lee/Bureau/mpg/data/liga/j18.csv")
        if actualDataBase != self._leagueItem.getDataBase():
            self._mercatoWidget.update()
