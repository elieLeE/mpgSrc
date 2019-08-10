# coding=utf-8

from gui import application
from gui import main_window


def main():
    app = application.GuiApplication()
    app.initialize()

    mainWindow = main_window.MainWindow(app)
    app.getWindowManager().registerMainWindow(mainWindow)
    mainWindow.showMaximized()
    # mainWindow.show()
    app.startApp()


if __name__ == "__main__":
    main()
