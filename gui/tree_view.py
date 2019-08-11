# coding=utf-8

from PySide2 import QtWidgets, QtCore, QtGui


class TreeView(QtWidgets.QTreeView):
    def __init__(self, treeViewColumnEnum, parent):
        super(TreeView, self).__init__(parent)
        self._treeViewColumnEnum = treeViewColumnEnum

    def _setHeader(self):
        self.model().setHorizontalHeaderLabels([v.value[1] for v in list(self._treeViewColumnEnum)])

    def _getNewItemsList(self, playerItemClass, dataItem):
        return [playerItemClass(dataItem) for _ in list(self._treeViewColumnEnum)]

    def clear(self):
        super(TreeView, self).clear()
        self._setHeader()
