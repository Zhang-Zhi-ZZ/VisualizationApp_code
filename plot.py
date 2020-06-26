import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from cc import Ui_widget


class MyMainForm(QMainWindow, Ui_widget):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        #self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        font = self.tableWidget.horizontalHeader().font()
        font.setBold(True)
        self.tableWidget.horizontalHeader().setFont(font)
        self.tableWidget.horizontalHeader().resizeSection(0,100)
        self.tableWidget.horizontalHeader().resizeSection(1,100)
        self.tableWidget.horizontalHeader().resizeSection(1,100)
        self.tableWidget.horizontalHeader().resizeSection(3,400)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        items = [['燕十三','21','Male','武林大俠'],['蕭十一郎','21','Male','武功好']]
        for i in range(len(items)):
            each_item = items[i]
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for j in range(len(each_item)):
                item = QTableWidgetItem(str(items[i][j]))
                if j != len(each_item) -1:
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    item.setForeground(QBrush(QColor(255,0,0)))
                else:
                    item.setBackground(QBrush(QColor(0,255,0)))
                self.tableWidget.setItem(row,j,item)

        self.tableWidget.setSpan(1,2,3,2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())