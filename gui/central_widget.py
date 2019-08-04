from PySide2 import QtWidgets


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        self.setupUi()

    def setupUi(self):
        label = QtWidgets.QLabel(self)
        label.setText("place holder")
