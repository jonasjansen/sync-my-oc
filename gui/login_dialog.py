from PyQt5 import QtWidgets
from gui.layouts import login_dialog
from gui.message_box import MessageBox


class LoginDialog(QtWidgets.QDialog, login_dialog.Ui_Dialog):

    was_canceled: bool = None
    has_login_data: bool = None

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.cancelButton.clicked.connect(self.cancel_button_clicked)
        self.okButton.clicked.connect(self.ok_button_clicked)
        self.setModal(True)
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.was_canceled = False
        self.has_login_data = False

    def ok_button_clicked(self):
        if not self.usernameInput.text() or not self.passwordInput.text():
            login_warning = MessageBox()
            login_warning.set_text("Warnung", "Bitte Benutzername und Passwort eingeben!")
            login_warning.show()
            login_warning.exec()
        else:
            self.has_login_data = True
            self.was_canceled = False
            self.close()
        return

    def cancel_button_clicked(self):
        self.was_canceled = True
        self.close()
        return

    def reject(self):
        """
        Will called every time the window is closed.
        So it should set self.was_canceled to True if there is no valid login data.
        """
        if not self.has_login_data:
            self.was_canceled = True
        super(self.__class__, self).reject()
