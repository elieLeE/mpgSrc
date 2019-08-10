# coding=utf-8

import pickle
from PySide2 import QtWidgets, QtCore, QtGui
from enum import Enum
from core.defines import Position


class MimeTypes(Enum):
    PLAYER = "Player"


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

        self.setDragEnabled(True)

    def updateTree(self, dataBaseInst):
        self._dataBaseInst = dataBaseInst

        self._model.clear()
        self._model.setHorizontalHeaderLabels([v.value[1] for v in list(DataBaseTreeViewColumn)])

        self._populate()
        self.update()

    def _populate(self):
        if self._dataBaseInst is not None:
            for playerInst in self._dataBaseInst.getAllPlayers():
                self._model.appendRow([DataBasePlayerItem(playerInst) for _ in list(DataBaseTreeViewColumn)])


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

    def _setHeader(self):
        self.setHorizontalHeaderLabels([v.value[1] for v in list(DataBaseTreeViewColumn)])

    def mimeData(self, indexes):
        """Return an object that contains serialized items of data corresponding to the list of indexes specified.
        The formats used to describe the encoded data is obtained from the mimeTypes() function.

        :param indexes: QModelIndex instance. represent the index of the item in the treeView we want to DAD.
        :return: QMimeData instance
        """
        self._mimeData = QtCore.QMimeData()
        playerInst = indexes[0].model().itemFromIndex(indexes[0]).getPlayerData()
        data = pickle.dumps({"playerData": playerInst})
        self._mimeData.setData(MimeTypes.PLAYER.value, data)
        return self._mimeData

    def clear(self):
        super(DataBaseTreeModel, self).clear()
        self._setHeader()


class TeamWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(TeamWidget, self).__init__(parent)

        self._teamTreeView = None
        self.setupUi()

        self.setAcceptDrops(True)

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)

        self._teamTreeView = TeamTreeView(self)
        layout.addWidget(self._teamTreeView)

    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasFormat(MimeTypes.PLAYER.value):
            mimeData = pickle.loads(mimeData.data(MimeTypes.PLAYER.value).data())
            # print(mimeData["playerData"].getName())
            # event.ignore()
            # return False
        event.accept()
        return True

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasFormat(MimeTypes.PLAYER.value):
            mimeData = pickle.loads(mimeData.data(MimeTypes.PLAYER.value).data())
            self._teamTreeView.addNewPlayer(mimeData["playerData"])
            # event.ignore()
            # return False

        event.accept()


class TeamTreeViewColumn(Enum):
    NAME = 0, "Name"
    EVAL_MOY = 1, "Note Moy"
    GAOL_NUMBER = 2, "Buts"
    PRIZE = 3, "Cote"
    PERCENT_TIT = 4, "Titulaire"


class TeamTreeView(QtWidgets.QTreeView):
    def __init__(self, parent):
        super(TeamTreeView, self).__init__(parent)

        self._model = QtGui.QStandardItemModel()
        self.setModel(self._model)

        self._model.setHorizontalHeaderLabels([v.value[1] for v in list(TeamTreeViewColumn)])

        self.populate()
        self.expandAll()

    def populate(self):
        self._model.appendRow(self._newTopLevelItemList(Position.GOAL.value))
        self._model.appendRow(self._newTopLevelItemList(Position.DEFENDER.value))
        self._model.appendRow(self._newTopLevelItemList(Position.MILIEU.value))
        self._model.appendRow(self._newTopLevelItemList(Position.STRIKER.value))

    def addNewPlayer(self, playerInst):
        globalPos = Position.getGloBasPos(playerInst.getPosition())
        topLevelItem = self._model.findItems(globalPos.value)
        if topLevelItem:
            topLevelItem[0].appendRow(self._newPlayerItemList(playerInst))

    def _newTopLevelItemList(self, topLevelName):
        return [TopLevelItem(topLevelName) for _ in list(TeamTreeViewColumn)]

    def _newPlayerItemList(self, playerInst):
        return [TeamPlayerItem(playerInst) for _ in list(TeamTreeViewColumn)]


class DataBasePlayerItem(QtGui.QStandardItem):
    def __init__(self, playerDataInst):
        super(DataBasePlayerItem, self).__init__()
        self._playerDataInst = playerDataInst

        self.setEditable(False)

    def getPlayerData(self):
        return self._playerDataInst

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
        return super(DataBasePlayerItem, self).data(role)


class TeamPlayerItem(QtGui.QStandardItem):
    def __init__(self, playerDataInst):
        super(TeamPlayerItem, self).__init__()
        self._playerDataInst = playerDataInst

    def data(self, role):
        if role == QtCore.Qt.DisplayRole:
            if self.column() == TeamTreeViewColumn.NAME.value[0]:
                return self._playerDataInst.getName()
            if self.column() == TeamTreeViewColumn.EVAL_MOY.value[0]:
                print("EVAL_MOY", self._playerDataInst.getEval())
                return self._playerDataInst.getEval()
            if self.column() == TeamTreeViewColumn.GAOL_NUMBER.value[0]:
                print("GAOL_NUMBER", self._playerDataInst.getGoalNumber())
                return self._playerDataInst.getGoalNumber()
            if self.column() == TeamTreeViewColumn.PRIZE.value[0]:
                print("PRIZE", self._playerDataInst.getPrize())
                return self._playerDataInst.getPrize()
            if self.column() == TeamTreeViewColumn.PERCENT_TIT.value[0]:
                print("PERCENT_TIT", self._playerDataInst.getPercentTit())
                return "{} %".format(self._playerDataInst.getPercentTit())
        return super(TeamPlayerItem, self).data(role)


class TopLevelItem(QtGui.QStandardItem):
    def __init__(self, topLevelName):
        super(TopLevelItem, self).__init__()

        self._topLevelName = topLevelName
        
    def data(self, role:int=...):
        if role == QtCore.Qt.DisplayRole:
            if self.column() == 0:
                return self._topLevelName
        return super(TopLevelItem, self).data(role)
