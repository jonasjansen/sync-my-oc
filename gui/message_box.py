from PyQt5 import QtWidgets, QtCore
from gui.layouts import message_box


class MessageBox(QtWidgets.QDialog, message_box.Ui_MessageBox):

    running_thread = None

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.running_thread = None

    def set_text(self, box_title, message):
        self.setWindowTitle(box_title)
        self.message.setText(message)

    def set_running_thread(self,running_thread: QtCore.QThread):
        self.running_thread = running_thread

    def closeEvent(self, event):
        if self.running_thread:
            self.running_thread.terminate()
