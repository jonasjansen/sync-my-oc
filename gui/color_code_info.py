from PyQt5 import QtWidgets
from gui.layouts import color_code_info


class ColorCodeInfo(QtWidgets.QDialog, color_code_info.Ui_Dialog):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.pushButton_green.setStyleSheet("background-color: green")
        self.pushButton_red.setStyleSheet("background-color: red")
        self.pushButton_blue.setStyleSheet("background-color: blue")
        self.pushButton_orange.setStyleSheet("background-color: orange")
        self.pushButton_violett.setStyleSheet("background-color: violet")
