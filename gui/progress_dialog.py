from PyQt5 import QtWidgets
from gui.layouts import progress_dialog


class ProgressDialog(QtWidgets.QDialog, progress_dialog.Ui_ProgressDialog):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setModal(True)
