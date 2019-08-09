# coding=utf-8

from PySide2 import QtWidgets


def testQApp():
    app = QtWidgets.QApplication([])

    w = QtWidgets.QWidget()
    w.show()

    a = QtWidgets.QFileDialog.getOpenFileName(w)

    app.exec_()


def testEnum():
    from enum import Enum
    class DataBaseTreeViewColumn(Enum):
        NAME = 1, "Name"
        POSITION = 2, "Poste"
        TEAM = 3, "Equipe"
        EVAL_MOY = 4, "Note Moy"
        GAOL_NUMBER = 5, "Buts"
        PRIZE = 6, "Cote"
        PERCENT_TIT = 7, "Titulaire"

    print(list(DataBaseTreeViewColumn))


def main():
    testEnum()


if __name__ == "__main__":
    main()
