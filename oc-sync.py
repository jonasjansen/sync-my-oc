import sys
from PyQt5 import QtWidgets
from gui.main_form import MainForm


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
