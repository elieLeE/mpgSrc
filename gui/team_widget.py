# coding=utf-8
from builtins import super

from PySide2 import QtWidgets, QtCore, QtGui
from enum import Enum
import pickle
from core.defines import Position, MAX_SUM_PRIZE_TEAM
from model.players import Player
from gui import widgets
from gui.tree_view import TreeView
from gui.defines import MimeTypes, UserRoles, LayoutType


class TeamWidget(QtWidgets.QWidget):
    newPlayerDropped = QtCore.Signal(str)

    def __init__(self, parent):
        super(TeamWidget, self).__init__(parent)

        self._playersDict = {}   # temporary. take team of league !

        self._totalPrizeEdit = None
        self._teamTreeView = None
        self.setupUi()

        self.setAcceptDrops(True)

        self._updateTotal()

        self._teamTreeView.teamChanged.connect(self._changeCompoTeam)
        self._teamTreeView.playerPrizeChanged.connect(self._updateTotal)

    def setupUi(self):
        layout = widgets.getConfiguredLayout(LayoutType.VERTICAL.value, parent=self)

        horizontalLayout = widgets.getConfiguredLayout(LayoutType.HORIZONTAL.value, margins=[0])
        totalPrizeLabel = QtWidgets.QLabel(self)
        totalPrizeLabel.setText("Total")
        horizontalLayout.addWidget(totalPrizeLabel)

        self._totalPrizeEdit = QtWidgets.QLineEdit(self)
        self._totalPrizeEdit.setReadOnly(True)
        self._totalPrizeEdit.setFixedWidth(80)
        horizontalLayout.addWidget(self._totalPrizeEdit)

        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        horizontalLayout.addItem(spacerItem)

        layout.addLayout(horizontalLayout)

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

    def _changeCompoTeam(self, playerInst):
        if playerInst is not None:
            if playerInst.getId() not in self._playersDict:
                self._playersDict[playerInst.getId()] = playerInst
            else:
                del self._playersDict[playerInst.getId()]
        self._updateTotal()

    def _updateTotal(self):
        newSum = 0
        for playerInst in self._playersDict.values():
            newSum += playerInst.getBuyPrize()
        self._totalPrizeEdit.setText(str(newSum))

        if newSum > MAX_SUM_PRIZE_TEAM:
            self._totalPrizeEdit.setStyleSheet("color: red;")
        else:
            self._totalPrizeEdit.setStyleSheet("color: black;")


class TeamTreeViewColumn(Enum):
    NAME = 0, "Name"
    EVAL_MOY = NAME[0] + 1, "Note Moy"
    GAOL_NUMBER = EVAL_MOY[0] + 1, "Buts"
    PERCENT_TIT = GAOL_NUMBER[0] + 1, "Titulaire"
    PRIZE = PERCENT_TIT[0] + 1, "Prix min \ actuel"
    CLOSE = PRIZE[0] + 1, "Close"


class TeamTreeView(TreeView):
    teamChanged = QtCore.Signal(Player)
    playerPrizeChanged = QtCore.Signal()

    def __init__(self, parent):
        super(TeamTreeView, self).__init__(TeamTreeViewColumn, parent)

        self.setModel(QtGui.QStandardItemModel())
        self._setHeader()

        closeButtonDelegate = CloseButtonTreeViewDelegate(self)
        self.setItemDelegateForColumn(TeamTreeViewColumn.CLOSE.value[0], closeButtonDelegate)
        closeButtonDelegate.buttonClicked.connect(self._removePlayer)

        prizeEditDelegate = PrizeEditDelegate(self)
        self.setItemDelegateForColumn(TeamTreeViewColumn.PRIZE.value[0], prizeEditDelegate)
        prizeEditDelegate.commitData.connect(self._playerPrizeChanged)

        self._populate()
        self.expandAll()

    def _populate(self):
        self.sourceModel().appendRow(self._getNewItemsList(PositionItem, Position.GOAL.value))
        self.sourceModel().appendRow(self._getNewItemsList(PositionItem, Position.DEFENDER.value))
        self.sourceModel().appendRow(self._getNewItemsList(PositionItem, Position.MILIEU.value))
        self.sourceModel().appendRow(self._getNewItemsList(PositionItem, Position.STRIKER.value))

    def addNewPlayer(self, playerInst):
        globalPos = Position.getGloBasPos(playerInst.getPosition())
        posItemIndex = self._getIndexes(UserRoles.ID_ROLE.value, globalPos)
        if len(posItemIndex) == 1:
            posItem = self.sourceModel().itemFromIndex(posItemIndex[0])
            if posItem:
                posItem.appendRow(self._getNewPlayerItemsList(playerInst))
                self.teamChanged.emit(playerInst)

    def hasAlreadyPlayer(self, playerInst):
        return len(self._getIndexes(UserRoles.ID_ROLE.value, playerInst.getId())) == 1

    def _getNewPlayerItemsList(self, playerInst):
        playerItemsList = self._getNewItemsList(TeamPlayerItem, playerInst)
        for item in playerItemsList:
            item.setEditable(False)
        playerItemsList[TeamTreeViewColumn.PRIZE.value[0]].setEditable(True)
        return playerItemsList

    def _removePlayer(self, indexItem):
        playerItem = self.model().itemFromIndex(indexItem)
        if playerItem is not None:
            playerInst = playerItem.getPlayerInst()
            self.teamChanged.emit(playerInst)
        self.model().removeRow(indexItem.row(), indexItem.parent())

    def _playerPrizeChanged(self, editor):
        self.playerPrizeChanged.emit()


class PrizeEditDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        super(PrizeEditDelegate, self).__init__(parent)

        self._actualPrize = -1
        self._firstState = True

    # def createEditor(self, parent, options, index):
    #     def _textChanged():
    #         print(editor.text())
    #         print("textChanged")
    #         if self._firstState:
    #             editor.setText("47 ")
    #             self._firstState = False
    #
    #     editor = QtWidgets.QLineEdit(parent)
    #     editor.setText("47 ")
    #     editor.textChanged.connect(_textChanged)
    #     return editor

    def paint(self, painter, option, index):
        if not index.parent().isValid():
            return

        playerItem = index.model().itemFromIndex(index)
        if playerItem is None:
            raise Exception("Player has not been found")
        playerDataInst = playerItem.getPlayerInst()

        rect = option.rect

        rect1 = QtCore.QRect(rect.x(), rect.y(), rect.width()/2, rect.height())
        rect1.setHeight(15)
        painter.setPen(QtCore.Qt.gray)
        painter.drawText(rect1, QtCore.Qt.AlignCenter, str(playerDataInst.getOffPrize()))

        rect2 = QtCore.QRect(rect.x() + rect1.width(), rect.y(), rect.width() / 2, rect.height())
        rect2.setHeight(15)
        actualPrize = self._actualPrize if self._actualPrize != -1 else playerDataInst.getBuyPrize()
        if actualPrize >= playerDataInst.getOffPrize():
            painter.setPen(QtCore.Qt.black)
        else:
            painter.setPen(QtCore.Qt.red)
        painter.drawText(rect2, QtCore.Qt.AlignCenter, str(playerDataInst.getBuyPrize()))

        painter.drawText(rect, QtCore.Qt.AlignCenter, '\\')

    # def editorEvent(self, event, model, option, index):
    #     if event.type() == QtCore.QEvent.MouseButtonPress and event.type() == QtCore.QEvent.MouseButtonRelease:
    #         self._actualPrize = -1
    #         # return True
    #
    #     if event.type() == QtGui.QKeyEvent:
    #         print("here")
    #
    #     # return True
    #     # return super(PrizeEditDelegate, self).editorEvent(event, model, option, index)


class CloseButtonTreeViewDelegate(QtWidgets.QStyledItemDelegate):
    buttonClicked = QtCore.Signal(QtCore.QModelIndex)

    _state = QtWidgets.QStyle.State_Enabled

    def __init__(self, parent):
        super(CloseButtonTreeViewDelegate, self).__init__(parent)

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
                return self._playerDataInst.getOffPrize()
        elif role == UserRoles.ID_ROLE.value:
            return self._playerDataInst.getId()
        return super(TeamPlayerItem, self).data(role)

    def setData(self, value, role:int=...):
        if self.column() == TeamTreeViewColumn.PRIZE.value[0]:
            self._playerDataInst.setBuyPrize(int(value))

    def getPlayerInst(self):
        return self._playerDataInst


class PositionItem(QtGui.QStandardItem):
    def __init__(self, topLevelName):
        super(PositionItem, self).__init__()

        self._posName = topLevelName
        self._minChildrenNumber = "2" if topLevelName == Position.GOAL.value else "6" \
            if topLevelName in [Position.DEFENDER.value, Position.MILIEU.value] else "4"

    def data(self, role: int = ...):
        if role == QtCore.Qt.DisplayRole:
            if self.column() == TeamTreeViewColumn.NAME.value[0]:
                return "{} - {} \\ {}".format(self._posName, self.rowCount(), self._minChildrenNumber)
        elif role == UserRoles.ID_ROLE.value:
            return self._posName
        return super(PositionItem, self).data(role)
