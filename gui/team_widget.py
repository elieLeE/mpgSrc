# coding=utf-8
from builtins import super

from PySide2 import QtWidgets, QtCore, QtGui
from enum import Enum
import pickle
from core.defines import Position
from gui.tree_view import TreeView
from gui.defines import MimeTypes, UserRoles


class TeamWidget(QtWidgets.QWidget):
    newPlayerDropped = QtCore.Signal(str)

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
            playerData = mimeData["playerData"]
            self._teamTreeView.addNewPlayer(playerData)

            self.newPlayerDropped.emit(playerData.getId())

            event.accept()
            return
        event.ignore()


class TeamTreeViewColumn(Enum):
    NAME = 0, "Name"
    EVAL_MOY = NAME[0] + 1, "Note Moy"
    GAOL_NUMBER = EVAL_MOY[0] + 1, "Buts"
    PERCENT_TIT = GAOL_NUMBER[0] + 1, "Titulaire"
    PRIZE = PERCENT_TIT[0] + 1, "Prix"
    CLOSE = PRIZE[0] + 1, "Close"


class TeamTreeView(TreeView):
    def __init__(self, parent):
        super(TeamTreeView, self).__init__(TeamTreeViewColumn, parent)

        self.setModel(QtGui.QStandardItemModel())
        self._setHeader()

        closeButtonDelegate = CloseButtonTreeViewDelegate()
        self.setItemDelegateForColumn(TeamTreeViewColumn.CLOSE.value[0], closeButtonDelegate)
        closeButtonDelegate.buttonClicked.connect(self.buttonClicked)

        self._populate()
        self.expandAll()

    def buttonClicked(self, indexItem):
        self.model().removeRow(indexItem.row(), indexItem.parent())

    def _populate(self):
        self.sourceModel().appendRow(self._getNewItemsList(TopLevelItem, Position.GOAL.value))
        self.sourceModel().appendRow(self._getNewItemsList(TopLevelItem, Position.DEFENDER.value))
        self.sourceModel().appendRow(self._getNewItemsList(TopLevelItem, Position.MILIEU.value))
        self.sourceModel().appendRow(self._getNewItemsList(TopLevelItem, Position.STRIKER.value))

    def addNewPlayer(self, playerInst):
        globalPos = Position.getGloBasPos(playerInst.getPosition())
        topLevelItem = self.sourceModel().findItems(globalPos.value, column=TeamTreeViewColumn.NAME.value[0])
        if topLevelItem:
            topLevelItem[0].appendRow(self._getNewPlayerItemsList(playerInst))

    def hasAlreadyPlayer(self, playerInst):
        return len(self._getItems(UserRoles.ID_ROLE.value, playerInst.getId())) == 1

    def _getNewPlayerItemsList(self, playerInst):
        playerItemsList = self._getNewItemsList(TeamPlayerItem, playerInst)
        for item in playerItemsList:
            item.setEditable(False)
        playerItemsList[TeamTreeViewColumn.PRIZE.value[0]].setEditable(True)
        return playerItemsList


class CloseButtonTreeViewDelegate(QtWidgets.QStyledItemDelegate):
    buttonClicked = QtCore.Signal(QtCore.QModelIndex)

    _state = QtWidgets.QStyle.State_Enabled

    def __init__(self):
        super(CloseButtonTreeViewDelegate, self).__init__()

    def paint(self, painter, option, index):
        if not index.parent().isValid():
            return

        text = "Delete"
        rect = option.rect

        textRect = QtCore.QRect(rect)
        textRect.setHeight(15)
        painter.drawText(textRect, text)

        buttonRect = QtCore.QRect(rect)
        buttonRect.setY(textRect.y())
        buttonRect.setHeight(15)

        button = QtWidgets.QStyleOptionButton()
        button.rect = buttonRect
        button.text = text
        button.state = CloseButtonTreeViewDelegate._state | QtWidgets.QStyle.State_Enabled

        QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_PushButton, button, painter)

    def editorEvent(self, event, model, option, index):
        if event.type() != QtCore.QEvent.MouseButtonPress and event.type() != QtCore.QEvent.MouseButtonRelease:
            # ignore
            CloseButtonTreeViewDelegate._state = QtWidgets.QStyle.State_Raised
            return True

        buttonRect = QtCore.QRect(option.rect)
        buttonRect.setY(option.rect.y())
        buttonRect.setHeight(15)

        if not buttonRect.contains(event.pos()):
            CloseButtonTreeViewDelegate._state = QtWidgets.QStyle.State_Raised
            return True

        if event.type() == QtCore.QEvent.MouseButtonPress:
            CloseButtonTreeViewDelegate._state = QtWidgets.QStyle.State_Sunken
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            CloseButtonTreeViewDelegate._state = QtWidgets.QStyle.State_Raised
            self.buttonClicked.emit(index)

        return True


class TeamPlayerItem(QtGui.QStandardItem):
    def __init__(self, playerDataInst):
        super(TeamPlayerItem, self).__init__()
        self._playerDataInst = playerDataInst

        if self.column() != TeamTreeViewColumn.PRIZE.value:
            self.setEditable(False)

    def data(self, role):
        if role == QtCore.Qt.DisplayRole:
            if self.column() == TeamTreeViewColumn.NAME.value[0]:
                return self._playerDataInst.getName()
            if self.column() == TeamTreeViewColumn.EVAL_MOY.value[0]:
                return self._playerDataInst.getEval()
            if self.column() == TeamTreeViewColumn.GAOL_NUMBER.value[0]:
                return self._playerDataInst.getGoalNumber()
            if self.column() == TeamTreeViewColumn.PERCENT_TIT.value[0]:
                return "{} %".format(self._playerDataInst.getPercentTit())
            if self.column() == TeamTreeViewColumn.PRIZE.value[0]:
                return self._playerDataInst.getPrize()
        elif role == UserRoles.ID_ROLE.value:
            return self._playerDataInst.getId()
        return super(TeamPlayerItem, self).data(role)


class TopLevelItem(QtGui.QStandardItem):
    def __init__(self, topLevelName):
        super(TopLevelItem, self).__init__()

        self._topLevelName = topLevelName

    def data(self, role: int = ...):
        if role == QtCore.Qt.DisplayRole:
            if self.column() == TeamTreeViewColumn.NAME.value[0]:
                return self._topLevelName
        return super(TopLevelItem, self).data(role)
