from PyQt5 import QtWidgets

class CustomMessageBox(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Logout')
        self.setStyleSheet("background-color: white;")

        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel('Are you sure you want to logout?', self)
        layout.addWidget(label)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Yes | QtWidgets.QDialogButtonBox.No)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    @staticmethod
    def question(parent=None):
        dialog = CustomMessageBox(parent)
        result = dialog.exec_()
        return result == QtWidgets.QDialog.Accepted
   