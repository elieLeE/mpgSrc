# coding=utf-8

from PySide2 import QtWidgets


def test():
    app = QtWidgets.QApplication([])

    w = QtWidgets.QWidget()
    w.show()

    a = QtWidgets.QFileDialog.getOpenFileName(w)

    app.exec_()


def main():
    test()


if __name__ == "__main__":
    main()
