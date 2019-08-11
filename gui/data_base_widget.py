# coding=utf-8

from PySide2 import QtWidgets, QtCore, QtGui
from enum import Enum
import pickle
from gui.tree_view import TreeView
from gui.defines import MimeTypes


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


class DataBaseTreeView(TreeView):
    def __init__(self, dataBaseInst, parent):
        super(DataBaseTreeView, self).__init__(DataBaseTreeViewColumn, parent)

        self._dataBaseInst = dataBaseInst

        self.setModel(DataBaseTreeModel())

        self.setDragEnabled(True)

    def updateTree(self, dataBaseInst):
        self._dataBaseInst = dataBaseInst

        self.model().clear()

        self._populate()
        self.update()

    def _populate(self):
        if self._dataBaseInst is not None:
            for playerInst in self._dataBaseInst.getAllPlayers():
                self.model().appendRow(self._getNewPlayerItemsList(DataBasePlayerItem, playerInst))


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
        mimeData = QtCore.QMimeData()
        playerInst = indexes[0].model().itemFromIndex(indexes[0]).getPlayerData()
        data = pickle.dumps({"playerData": playerInst})
        mimeData.setData(MimeTypes.PLAYER.value, data)
        return mimeData

    def clear(self):
        super(DataBaseTreeModel, self).clear()
        self._setHeader()


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
