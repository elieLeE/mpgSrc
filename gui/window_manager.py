from PySide2 import QtWidgets


class WindowManager(object):
    def __init__(self, application, mainWindow):
        super(WindowManager, self).__init__()

        self._application = application
        self._mainWindow = mainWindow
