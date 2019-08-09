# coding=utf-8

from PySide2 import QtWidgets
from gui.central_widget import CentralWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, application, parent=None):
        super(MainWindow, self).__init__(parent)

        self._application = application

        self._appExplorerDW = None
        self._leaguesExplorer = None
        self._centralWidget = None

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

        toolbar = QtWidgets.QToolBar(self.tr("Tool bar"), self)
        toolbar.setMovable(False)

        convertDataBaeAction = toolbar.addAction("Create new league")
        convertDataBaeAction.triggered.connect(self._application.getWindowManager().createNewLeague)

        loadLeagueAction = toolbar.addAction("Load league")
        loadLeagueAction.setDisabled(True)

        toolbar.addSeparator()

        convertDataBaeAction = toolbar.addAction("Convert data base")
        convertDataBaeAction.triggered.connect(self._application.getWindowManager().convertMPGDataBase)

        self.addToolBar(toolbar)

    def addLeagueItem(self, newLeagueItem):
        self._centralWidget.addNewTabLeague(newLeagueItem, self._application.getApplicationManager())
