# coding=utf-8
from gui import widgets
from gui.defines import LayoutType
from PySide2 import QtWidgets
from gui.mercato_widget import MercatoWidget
from gui.league_info_widget import LeagueInfoWidget


class LeagueWidget(QtWidgets.QWidget):
    def __init__(self, leagueInst, applicationManager, parent):
        super(LeagueWidget, self).__init__(parent)
        self._leagueInst = leagueInst
        self._applicationManager = applicationManager

        self._label = None
        self._mercatoWidget = None
        self._leagueInfoWidget = None

        self.setupUi()
        self._chooseDataBase()

    def setupUi(self):
        mainLayout = widgets.getConfiguredLayout(LayoutType.VERTICAL.value, parent=self)

        toolbar = QtWidgets.QToolBar(self.tr("Tool bar"), self)
        toolbar.setStyleSheet("QToolBar {background-color: grey;}")
        toolbar.setMovable(False)

        chooseDataBase = toolbar.addAction("Choose data base")
        chooseDataBase.triggered.connect(self._chooseDataBase)

        mainLayout.addWidget(toolbar)

        tabWidget = QtWidgets.QTabWidget(self)
        self._mercatoWidget = MercatoWidget(self._leagueInst.getMercato(), self)
        tabWidget.addTab(self._mercatoWidget, "Mercato")

        self._leagueInfoWidget = LeagueInfoWidget(self._leagueInst, self)
        tabWidget.addTab(self._leagueInfoWidget, "League info")

        tabWidget.setTabEnabled(1, False)
        mainLayout.addWidget(tabWidget)

    def _chooseDataBase(self):
        actualDataBase = self._leagueInst.getMercato().getDataBase()
        dataBaseInst = self._applicationManager.loadDataBaseInLeague(self._leagueInst, r"/home/lee/Bureau/mpg/data/premier_league/j38.csv")
        if actualDataBase != dataBaseInst:
            self._leagueInst.getMercato().setDataBase(dataBaseInst)
            self._mercatoWidget.update()
