import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog
from PyQt5.QtCore import Qt

class DialogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dialog')
        self.resize(350, 300)

        self.btn = QPushButton(self)
        self.btn.setText('弹出对话框')
        self.btn.move(50, 50)
        self.btn.clicked.connect(self.showDialog)

        self.show()

    def showDialog(self):
        dialog = QDialog()
        btn = QPushButton('ok', dialog)
        btn.move(50, 50)
        dialog.setWindowTitle('Dialog')
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DialogWindow()
    sys.exit(app.exec_())