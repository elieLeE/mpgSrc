# coding=utf-8

from PySide2 import QtWidgets, QtCore, QtGui
from enum import Enum


class MercatoWidget(QtWidgets.QWidget):
    def __init__(self, leagueItem, parent):
        super(MercatoWidget, self).__init__(parent)

        self._leagueItem = leagueItem

        self._viewDataBaseWidget = None

        self.setupUi()

    def setupUi(self):
        mainLayout = QtWidgets.QVBoxLayout(self)

        toolbar = QtWidgets.QToolBar(self.tr("Tool bar"), self)
        toolbar.setStyleSheet("QToolBar {background-color: grey;}")
        toolbar.setMovable(False)

        # chooseDataBase = toolbar.addAction("Choose data base")
        # chooseDataBase.triggered.connect(self._chooseDataBase)

        addMercatoTurn = toolbar.addAction("Add mercato turn")
        addMercatoTurn.triggered.connect(self._addMercatoTurn)

        mainLayout.addWidget(toolbar)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.setStyleSheet("QSplitter::handle {background-color: black;}")
        self._viewDataBaseWidget = ViewDataBaseWidget(self._leagueItem.getDataBase(), self)
        splitter.addWidget(self._viewDataBaseWidget)
        splitter.addWidget(TeamWidget(self))
        mainLayout.addWidget(splitter)

    def update(self):
        self._viewDataBaseWidget.updateWidget(self._leagueItem.getDataBase())

    def _addMercatoTurn(self):
        print("mercato turn")


class ViewDataBaseWidget(QtWidgets.QWidget):
    def __init__(self, dataBaseInst, parent):
        super(ViewDataBaseWidget, self).__init__(parent)
        self._dataBaseInst = dataBaseInst

        self._dataBaseTreeView = None

        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)

        self._dataBaseTreeView = DataBaseTreeView(self._dataBaseInst, self)
        layout.addWidget(self._dataBaseTreeView)

    def updateWidget(self, dataBaseInst):
        self._dataBaseTreeView.updateTree(dataBaseInst)


class DataBaseTreeViewColumn(Enum):
    NAME = 0, "Name"
    POSITION = 1, "Poste"
    TEAM = 2, "Equipe"
    EVAL_MOY = 3, "Note Moy"
    GAOL_NUMBER = 4, "Buts"
    PRIZE = 5, "Cote"
    PERCENT_TIT = 6, "Titulaire"


class DataBaseTreeView(QtWidgets.QTreeView):
    def __init__(self, dataBaseInst, parent):
        super(DataBaseTreeView, self).__init__(parent)

        self._dataBaseInst = dataBaseInst

        self._model = DataBaseTreeModel()
        self.setModel(self._model)

    def updateTree(self, dataBaseInst):
        self._dataBaseInst = dataBaseInst

        self._model.clear()
        self._model.setHorizontalHeaderLabels([v.value[1] for v in list(DataBaseTreeViewColumn)])

        self._populate()
        self.update()

    def _populate(self):
        if self._dataBaseInst is not None:
            for playerInst in self._dataBaseInst.getAllPlayers():
                self._model.appendRow([PlayerItem(playerInst) for _ in list(DataBaseTreeViewColumn)])


class DataBaseTreeModel(QtGui.QStandardItemModel):
    def __init__(self):
        super(DataBaseTreeModel, self).__init__()
        self._setHeader()

    def data(self, index, role):
        if role == QtCore.Qt.BackgroundRole:
            if index.row() % 2 == 0:
                return QtGui.QColor(226, 237, 253)
            return QtCore.Qt.white
        return super(DataBaseTreeModel, self).data(index, role)

    def clear(self):
        super(DataBaseTreeModel, self).clear()
        self._setHeader()

    def _setHeader(self):
        self.setHorizontalHeaderLabels([v.value[1] for v in list(DataBaseTreeViewColumn)])


class PlayerItem(QtGui.QStandardItem):
    def __init__(self, playerDataInst):
        super(PlayerItem, self).__init__()
        self._playerDataInst = playerDataInst

    def data(self, role):
        if role == QtCore.Qt.DisplayRole:
            if self.column() == DataBaseTreeViewColumn.NAME.value[0]:
                return self._playerDataInst.getName()
            if self.column() == DataBaseTreeViewColumn.POSITION.value[0]:
                return self._playerDataInst.getPosition()
            if self.column() == DataBaseTreeViewColumn.TEAM.value[0]:
                return self._playerDataInst.getTeam().getId()
            if self.column() == DataBaseTreeViewColumn.EVAL_MOY.value[0]:
                return self._playerDataInst.getEval()
            if self.column() == DataBaseTreeViewColumn.GAOL_NUMBER.value[0]:
                return self._playerDataInst.getGoalNumber()
            if self.column() == DataBaseTreeViewColumn.PRIZE.value[0]:
                return self._playerDataInst.getPrize()
            if self.column() == DataBaseTreeViewColumn.PERCENT_TIT.value[0]:
                return "{} %".format(self._playerDataInst.getPercentTit())
        return super(PlayerItem, self).data(role)


class TeamWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(TeamWidget, self).__init__(parent)

        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(TeamTreeView(self))


class TeamTreeView(QtWidgets.QTreeView):
    def __init__(self, parent):
        super(TeamTreeView, self).__init__(parent)

        self._model = QtGui.QStandardItemModel()
        self.setModel(self._model)

        self._model.setHorizontalHeaderLabels(["Column 1"])

        self.populate()

    def populate(self):
        self._model.appendRow(QtGui.QStandardItem("Gaols"))
        self._model.appendRow(QtGui.QStandardItem("Def"))
        self._model.appendRow(QtGui.QStandardItem("Mil"))
        self._model.appendRow(QtGui.QStandardItem("Att"))
