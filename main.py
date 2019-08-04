# coding=utf-8

from gui import application
from gui import main_window


def main():
    print("MPG")

    app = application.GuiApplication()
    app.initialize()

    mainWindow = main_window.MainWindow(app)
    # mainWindow.showMaximized()
    mainWindow.show()
    app.startApp()


if __name__ == "__main__":
    main()
