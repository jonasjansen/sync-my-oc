# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 138)
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 381, 81))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.usernameLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.usernameLabel.setObjectName("usernameLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.usernameLabel)
        self.usernameInput = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.usernameInput.setObjectName("usernameInput")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.usernameInput)
        self.passwordLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.passwordLabel.setObjectName("passwordLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordInput = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.passwordInput.setObjectName("passwordInput")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.passwordInput)
        self.okButton = QtWidgets.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(10, 100, 191, 28))
        self.okButton.setObjectName("okButton")
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setGeometry(QtCore.QRect(210, 100, 181, 28))
        self.cancelButton.setObjectName("cancelButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login"))
        self.usernameLabel.setText(_translate("Dialog", "Name"))
        self.passwordLabel.setText(_translate("Dialog", "Passwort"))
        self.okButton.setText(_translate("Dialog", "Ok"))
        self.cancelButton.setText(_translate("Dialog", "Abbrechen"))

