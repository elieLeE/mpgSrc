# coding=utf-8

from PySide2 import QtWidgets, QtCore, QtGui
from enum import Enum
import pickle
from core.defines import Position
from gui.tree_view import TreeView
from gui.defines import MimeTypes, UserRoles


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
            if not self._teamTreeView.hasAlreadyPlayer(mimeData["playerData"]):
                event.accept()
                return
        event.ignore()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasFormat(MimeTypes.PLAYER.value):
            mimeData = pickle.loads(mimeData.data(MimeTypes.PLAYER.value).data())
            self._teamTreeView.addNewPlayer(mimeData["playerData"])
            event.accept()
            return
        event.ignore()


class TeamTreeViewColumn(Enum):
    NAME = 0, "Name"
    EVAL_MOY = 1, "Note Moy"
    GAOL_NUMBER = 2, "Buts"
    PRIZE = 3, "Prix"
    PERCENT_TIT = 4, "Titulaire"


class TeamTreeView(TreeView):
    def __init__(self, parent):
        super(TeamTreeView, self).__init__(TeamTreeViewColumn, parent)

        self.setModel(QtGui.QStandardItemModel())
        self._setHeader()

        self._populate()
        self.expandAll()

    def _populate(self):
        self.model().appendRow(self._getNewPlayerItemsList(TopLevelItem, Position.GOAL.value))
        self.model().appendRow(self._getNewPlayerItemsList(TopLevelItem, Position.DEFENDER.value))
        self.model().appendRow(self._getNewPlayerItemsList(TopLevelItem, Position.MILIEU.value))
        self.model().appendRow(self._getNewPlayerItemsList(TopLevelItem, Position.STRIKER.value))

    def addNewPlayer(self, playerInst):
        globalPos = Position.getGloBasPos(playerInst.getPosition())
        topLevelItem = self.model().findItems(globalPos.value)
        if topLevelItem:
            topLevelItem[0].appendRow(self._getNewPlayerItemsList(TeamPlayerItem, playerInst))

    def hasAlreadyPlayer(self, playerInst):
        return len(self.model().match(self.model().index(0, 0),
                                      UserRoles.ID_ROLE.value,
                                      playerInst.getId(),
                                      flags=QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)) == 1


class TeamPlayerItem(QtGui.QStandardItem):
    def __init__(self, playerDataInst):
        super(TeamPlayerItem, self).__init__()
        self._playerDataInst = playerDataInst

    def data(self, role):
        if role == QtCore.Qt.DisplayRole:
            if self.column() == TeamTreeViewColumn.NAME.value[0]:
                return self._playerDataInst.getName()
            if self.column() == TeamTreeViewColumn.EVAL_MOY.value[0]:
                return self._playerDataInst.getEval()
            if self.column() == TeamTreeViewColumn.GAOL_NUMBER.value[0]:
                return self._playerDataInst.getGoalNumber()
            if self.column() == TeamTreeViewColumn.PRIZE.value[0]:
                return self._playerDataInst.getPrize()
            if self.column() == TeamTreeViewColumn.PERCENT_TIT.value[0]:
                return "{} %".format(self._playerDataInst.getPercentTit())
        elif role == UserRoles.ID_ROLE.value:
            return self._playerDataInst.getId()
        return super(TeamPlayerItem, self).data(role)


class TopLevelItem(QtGui.QStandardItem):
    def __init__(self, topLevelName):
        super(TopLevelItem, self).__init__()

        self._topLevelName = topLevelName

    def data(self, role: int = ...):
        if role == QtCore.Qt.DisplayRole:
            if self.column() == 0:
                return self._topLevelName
        return super(TopLevelItem, self).data(role)
