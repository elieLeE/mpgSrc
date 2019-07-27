# coding=utf-8

from gui import application


def main():
    print("MPG")

    app = application.GuiApplication()
    app.initialize()
    app.startApp()


if __name__ == "__main__":
    main()
