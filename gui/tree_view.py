# coding=utf-8

from PySide2 import QtWidgets, QtGui, QtCore


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

    def _getItems(self, role, v):
        return self.model().match(self.model().index(0, 0), role, v,
                                  flags=QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)

    def refresh(self):
        self.viewport().update()

    def clear(self):
        self.blockSignals(True)
        super(TreeView, self).clear()
        self._setHeader()
        self.blockSignals(False)
