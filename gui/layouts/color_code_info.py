# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'color_code_info.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(252, 189)
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 231, 171))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.pushButton_green = QtWidgets.QPushButton(self.formLayoutWidget)
        self.pushButton_green.setText("")
        self.pushButton_green.setObjectName("pushButton_green")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.pushButton_green)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label)
        self.pushButton_orange = QtWidgets.QPushButton(self.formLayoutWidget)
        self.pushButton_orange.setText("")
        self.pushButton_orange.setObjectName("pushButton_orange")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pushButton_orange)
        self.pushButton_red = QtWidgets.QPushButton(self.formLayoutWidget)
        self.pushButton_red.setText("")
        self.pushButton_red.setObjectName("pushButton_red")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.pushButton_red)
        self.pushButton_blue = QtWidgets.QPushButton(self.formLayoutWidget)
        self.pushButton_blue.setText("")
        self.pushButton_blue.setObjectName("pushButton_blue")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.pushButton_blue)
        self.pushButton_violett = QtWidgets.QPushButton(self.formLayoutWidget)
        self.pushButton_violett.setText("")
        self.pushButton_violett.setObjectName("pushButton_violett")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.pushButton_violett)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.label_5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Farbcodes"))
        self.label.setText(_translate("Dialog", "Neu"))
        self.label_2.setText(_translate("Dialog", "Lokal vorhanden"))
        self.label_3.setText(_translate("Dialog", "Lokal vorhanden und verändert"))
        self.label_4.setText(_translate("Dialog", "Online verändert"))
        self.label_5.setText(_translate("Dialog", "Lokal und online verändert"))


