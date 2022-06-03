# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'message_box.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MessageBox(object):
    def setupUi(self, MessageBox):
        MessageBox.setObjectName("MessageBox")
        MessageBox.resize(400, 67)
        self.message = QtWidgets.QLabel(MessageBox)
        self.message.setGeometry(QtCore.QRect(30, 20, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.message.setFont(font)
        self.message.setObjectName("message")

        self.retranslateUi(MessageBox)
        QtCore.QMetaObject.connectSlotsByName(MessageBox)

    def retranslateUi(self, MessageBox):
        _translate = QtCore.QCoreApplication.translate
        MessageBox.setWindowTitle(_translate("MessageBox", "Messsage"))
        self.message.setText(_translate("MessageBox", "Bitte Benutzername und Passwort eingeben!"))
