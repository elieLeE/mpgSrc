# coding=utf-8

from PySide2 import QtWidgets, QtGui
from gui.central_widget import CentralWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, application, parent=None):
        super(MainWindow, self).__init__(parent)

        self._application = application

        self._appExplorerDW = None
        self._leaguesExplorer = None
        self._centralWidget = None

        self._newLeagueAction = None
        self._loadLeagueAction = None

        self._convertDataBaeAction = None
        self._determineDayPerformances = None

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle(self._application.getApplicationManager().getName())

        self._centralWidget = CentralWidget(self)
        self.setCentralWidget(self._centralWidget)

        # Log Window

        # self.logWindow = LogWindow()
        # self.logWindow.useGlobalMessageHandler()
        # self.logWindowDock = QtWidgets.QDockWidget(self)
        # self.logWindowDock.setObjectName("_logDock")
        # self.logWindowDock.setWindowTitle(self.tr("Log window"))
        # self.logWindowDock.setWidget(self.logWindow)

        # Add dock widgets
        # self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._appExplorerDW)
        # self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.logWindowDock)
        # self.logWindowDock.hide()

        self.createActions()
        self.createToolBar()
        self.createMenus()

    def createActions(self):
        self._newLeagueAction = QtWidgets.QAction("Create new league")
        self._newLeagueAction.triggered.connect(self._application.getWindowManager().createNewLeague)

        self._loadLeagueAction = QtWidgets.QAction("Load league")
        self._loadLeagueAction.setDisabled(True)

        self._convertDataBaeAction = QtWidgets.QAction("Convert data base")
        self._convertDataBaeAction.triggered.connect(self._application.getWindowManager().convertMPGDataBase)

        self._determineDayPerformances = QtWidgets.QAction("Determine day performances")
        self._determineDayPerformances.triggered.connect(self._application.getWindowManager().determineDayPerformances)

    def createToolBar(self):
        toolbar = QtWidgets.QToolBar(self.tr("Tool bar"), self)
        toolbar.setMovable(False)

        toolbar.addAction(self._newLeagueAction)
        toolbar.addAction(self._loadLeagueAction)

        toolbar.addSeparator()

        toolbar.addAction(self._convertDataBaeAction)
        toolbar.addAction(self._determineDayPerformances)

        self.addToolBar(toolbar)

    def createMenus(self):
        fileMenu = self.menuBar().addMenu("&Leagues")
        fileMenu.addAction(self._newLeagueAction)
        fileMenu.addAction(self._loadLeagueAction)

        fileMenu = self.menuBar().addMenu("&Tools")
        fileMenu.addAction(self._convertDataBaeAction)
        fileMenu.addAction(self._determineDayPerformances)

    def addLeagueItem(self, newLeagueItem):
        self._centralWidget.addNewTabLeague(newLeagueItem, self._application.getApplicationManager())
