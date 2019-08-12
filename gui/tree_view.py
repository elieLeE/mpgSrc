# coding=utf-8

from PySide2 import QtWidgets, QtGui


class TreeView(QtWidgets.QTreeView):
    def __init__(self, treeViewColumnEnum, parent):
        super(TreeView, self).__init__(parent)
        self._treeViewColumnEnum = treeViewColumnEnum

    def sourceModel(self):
        model = self.model()
        if isinstance(model, QtGui.QStandardItemModel):
            return model
        return model.sourceModel()

    def _setHeader(self):
        self.sourceModel().setHorizontalHeaderLabels([v.value[1] for v in list(self._treeViewColumnEnum)])

    def _getNewItemsList(self, playerItemClass, dataItem):
        return [playerItemClass(dataItem) for _ in list(self._treeViewColumnEnum)]

    def clear(self):
        super(TreeView, self).clear()
        self._setHeader()
