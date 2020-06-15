import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Visualize it!"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 350
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setFixedSize(600,350)
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("McMaster.jpg")))
        self.setPalette(palette)

        App_logo = QLabel(self)
        App_logo.setGeometry(50, 80, 550, 250)
        App_logo.setObjectName("App_logo")
        logo = QtGui.QPixmap("logo.jpg").scaled(550, 250)
        App_logo.setPixmap(logo)

        start = QPushButton(self)
        start.setStyleSheet("QPushButton{border-image: url(start.jpg)}")
        start.setCursor(QCursor(Qt.PointingHandCursor))
        start.setGeometry(480,250,120,110)
        start.clicked.connect(self.startApp_onClick)

        self.show()

    @pyqtSlot()
    def startApp_onClick(self):
        self.statusBar().showMessage("Switched to window 1")
        self.cams = loadFile()
        self.cams.show()
        self.close()



    '''   
    @pyqtSlot()
    def buttonWindow1_onClick(self):
        self.statusBar().showMessage("Switched to window 1")
        self.cams = Window1(self.lineEdit1.text())
        self.cams.show()
        self.close()

    @pyqtSlot()
    def buttonWindow2_onClick(self):
        self.statusBar().showMessage("Switched to window 2")
        self.cams = Window2(self.lineEdit2.text())
        self.cams.show()
        self.close()
    '''

#选择文件，选择要不要display axis，确认plot
class loadFile(QDialog):

    def __init__(self,parent=None):
        #super().__init__(parent)
        super().__init__()
        self.setWindowTitle('Please select your input file(s)')
        #self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))
        self.setFixedSize(400,280)
        palette = QPalette()
        palette.setColor(QWidget().backgroundRole(), QColor(250,250,210))
        self.setPalette(palette)

        self.InputPoints = ''
        self.InputEdges = ''


        self.guide = QLabel(self)
        self.guide.setText('Input File Guidance: balabala\n'
                           'Please make sure your file contains: balabala\n'
                           'format for points: balabala\n'
                           'format for edges: balabala\n')
        self.guide.setStyleSheet("font: 10pt Helvetica")
        #self.guide.setGeometry(20, 20, 300, 80)

        self.pointFileLabel = QLabel(self)
        self.pointFileLabel.setText('Please select the file containing your point data:')
        self.pointFileLabel.setStyleSheet("font: 10pt Helvetica")
        #self.pointFileLabel.setGeometry(20, 100, 300, 20)

        self.pointFile = QPushButton(self)
        self.pointFile.setStyleSheet('background-color: rgb(245,255,250); color: #2F4F4F; font: 8pt Helvetica')
        self.pointFile.setText('Open')
        self.pointFile.clicked.connect(self.OpenPointFile)
        #self.pointFile.setGeometry(320,100,50,20)
        self.pointFile.setCursor(QCursor(Qt.PointingHandCursor))

        self.label1 = QLabel(self)
        self.label1.setGeometry(20, 120, 400, 40)
        self.label1.setFixedWidth(400)
        #self.label1.setText('')
        self.label1.setWordWrap(True)
        self.label1.setStyleSheet("font: 9pt Helvetica; color: #C0C0C0")


        self.edgeFileLabel = QLabel(self)
        self.edgeFileLabel.setText('Please select the file containing your edge data')
        #self.edgeFileLabel.setGeometry(20,155,300,20)
        self.edgeFileLabel.setStyleSheet("font: 10pt Helvetica")

        self.label2 = QLabel(self)
        self.label2.setGeometry(20,170,500,40)
        self.label2.setFixedWidth(400)
        self.label2.setWordWrap(True)
        #self.label2.setText('')
        self.label2.setStyleSheet("font: 9pt Helvetica; color: #C0C0C0")

        self.edgeFile = QPushButton(self)
        self.edgeFile.setStyleSheet('background-color: rgb(245,255,250); color: #2F4F4F; font: 8pt Helvetica')
        self.edgeFile.setText('Open')
        self.edgeFile.clicked.connect(self.OpenEdgeFile)
        #self.edgeFile.setGeometry(320, 150, 50, 20)
        self.edgeFile.setCursor(QCursor(Qt.PointingHandCursor))

        self.validateInput = QPushButton(self)
        #self.validateInput.setGeometry(20, 220, 130, 25)
        self.validateInput.clicked.connect(self.validate)
        self.validateInput.setCursor(QCursor(Qt.PointingHandCursor))
        self.validateInput.setText('Validate Input Data')
        self.validateInput.setStyleSheet('background-color: rgb(	255,0,0); color: #000000; font: 10pt Helvetica')

        self.next = QPushButton(self)
        #self.next.setGeometry(175,220,50,25)
        self.next.setCursor(QCursor(Qt.PointingHandCursor))
        self.next.setText('Plot')
        self.next.clicked.connect(self.msg)
        self.next.setStyleSheet('background-color: rgb(	255,0,0); color: #000000; font: 10pt Helvetica')

        self.message = QLabel(self)
        #self.message.setGeometry(225, 220, 160, 25)
        self.message.setText('')
        self.message.setStyleSheet('color: #000000; font: 8pt Helvetica')
        self.message.setWordWrap(True)

        horizontalLayout1 = QHBoxLayout()
        horizontalLayout1.addWidget(self.pointFileLabel)
        horizontalLayout1.addWidget(self.pointFile)

        horizontalLayout2 = QHBoxLayout()
        horizontalLayout2.addWidget(self.edgeFileLabel)
        horizontalLayout2.addWidget(self.edgeFile)

        horizontalLayout3 = QHBoxLayout()
        horizontalLayout3.addWidget(self.validateInput)
        horizontalLayout3.addWidget(self.next)
        horizontalLayout3.addWidget(self.message)

        verticalLayout = QVBoxLayout(self)
        verticalLayout.addWidget(self.guide)
        verticalLayout.addLayout(horizontalLayout1)
        verticalLayout.addWidget(self.label1)
        verticalLayout.addLayout(horizontalLayout2)
        verticalLayout.addWidget(self.label2)
        verticalLayout.addLayout(horizontalLayout3)

        self.setLayout(verticalLayout)

    def msg(self):
        self.message.setText("Please validate your input first!")


    def goMainWindow(self):
        self.cams = Window()
        self.cams.show()
        self.close()

    def OpenPointFile(self):
        #output： C:/Users/ZZ/PycharmProject/.../InputPoints.txt

        self.InputPoints = QFileDialog().getOpenFileName(None,"Open file", "", "Text Files (*.txt)")[0]
        self.label1.setText('Selected file: ' + str(self.InputPoints))

    def OpenEdgeFile(self):

        #output： C:/Users/ZZ/PycharmProject/.../InputPoints.txt
        self.InputEdges = QFileDialog().getOpenFileName(None,"Open file", "", "Text Files (*.txt)")[0]
        self.label2.setText('selected file: ' + str(self.InputEdges))

    def validate(self):
        # validate the data
        self.next.setStyleSheet('background-color: rgb(127,255,0); color: #000000; font: 10pt Helvetica')
        self.message.setText('')
        global pointsIsValid, edgeIsValid
        pointsIsValid, edgeIsValid = True, True
        if self.InputPoints!='':
            pointsIsValid = False
            with open(self.InputPoints, 'r') as f_in1:
                for line in f_in1:
                    records1 = line.split()
                    if len(records1) != 3:
                        self.message.setText('Your points file is invalid: Has more than 3 numbers in one row')
                        break
                    else:
                        pointsIsValid = True

        if self.InputEdges!='':
            edgeIsValid = False
            with open(self.InputEdges, 'r') as f_in2:
                for line in f_in2:
                    records2 = line.split()
                    if len(records2) != 3 + int(records2[1]) or len(records2) <= 3:
                        self.message.setText('Your edges file is invalid: Has more than 3 numbers in one row')
                        break
                    else:
                        edgeIsValid = True


        if pointsIsValid and edgeIsValid:
            self.next.clicked.connect(self.plot_onClick)

    @pyqtSlot()
    def plot_onClick(self):
        #self.cams = result()
        self.cams = result()
        self.cams.show()
        self.close()


class result(QMainWindow):

    global x_axis, y_axis, z_axis
    global line_x,line_y, line_z
    global show_axis,axis_status

    def __init__(self, parent=None):
        super(result, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Plot')
        self.add_menubar()
        self.add_content()



    def add_menubar(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction("New Plot")

        axis_off_action = QAction('Do not show axis', self)
        axis_off_action.triggered.connect(self.axis_off)
        axis_on_action = QAction('Show axis', self)
        axis_on_action.triggered.connect(self.axis_on)
        coord_off_action = QAction('Do not show point coordinates',self)
        coord_off_action.triggered.connect(self.coord_off)
        coord_on_action = QAction('Show point coordinates', self)
        coord_on_action.triggered.connect(self.coord_on)
        pointnum_off_action = QAction('Do not show point number',self)
        pointnum_off_action.triggered.connect(self.pointnum_off)
        pointnum_on_action = QAction('Show point number',self)
        pointnum_on_action.triggered.connect(self.pointnum_on)

        viewMenu = mainMenu.addMenu('View')

        axisMenu = viewMenu.addMenu('Axis')
        coordMenu = viewMenu.addMenu('Coordinates')
        pointMenu = viewMenu.addMenu('Point Number')
        axisMenu.addAction(axis_off_action)
        axisMenu.addAction(axis_on_action)
        coordMenu.addAction(coord_off_action)
        coordMenu.addAction(coord_on_action)
        pointMenu.addAction(pointnum_off_action)
        pointMenu.addAction(pointnum_on_action)



        editMenu = mainMenu.addMenu('Edit')
        editMenu.addAction("Permute Variables")
        editMenu.addAction("Change Variables")
        computeMenu = mainMenu.addMenu("Compute")
        computeMenu.addAction("Diameter")
        computeMenu.addAction("Shortest Path")
        helpMenu = mainMenu.addMenu("Help")
        helpMenu.addAction("Instructions")

    def add_content(self):
        #self.setWindowTitle('Plot')
        #self.setFixedSize(600,800)

        self.figure = plt.figure()
        self.figure.tight_layout()

        self.plotting = FigureCanvas(self.figure)
        self.plotting.resize(100,100)

        self.axis_status = 'on'
        self.show_coord = False
        self.show_pointnum = False
        self.vertices_analysis = QLabel(self)
        self.plot()
        self.toolbar = NavigationToolbar(self.plotting, self)
        self.toolbar.setGeometry(20,10,200,20)


        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(self.toolbar)
        verticalLayout.addWidget(self.plotting)
        verticalLayout.addWidget(self.vertices_analysis)

        #self.setLayout(verticalLayout)

        layout_widget = QWidget()
        layout_widget.setLayout(verticalLayout)
        self.setCentralWidget(layout_widget)
        #self.setGeometry(300, 300, 350, 300)
        #self.setWindowTitle('Plot')
        #self.show()


    def plot(self):
        global is_vertice, x_axis, y_axis, z_axis
        self.figure.clear()
        f = open("InputPoints_Example1.txt", "r")
        #print(loadFile.InputPoints)
        #f = open(loadFile.InputPoints,'r')
        x_axis = []
        y_axis = []
        z_axis = []
        for i in f:
            tmp = i.split()
            x_axis.append(int(tmp[0]))
            y_axis.append(int(tmp[1]))
            z_axis.append(int(tmp[2]))
        f.close()

        x_axis.append(0)
        y_axis.append(0)
        z_axis.append(0)

        x_axis.append(10)
        y_axis.append(10)
        z_axis.append(10)

        is_vertice = [0 for i in range(len(x_axis))]

        ax = self.figure.add_subplot(111, projection='3d')

        #if loadFile.InputEdges != '':

        f = open("InputEdges_Example1.txt", "r")
            #f = open(loadFile.InputEdges,'r')
        for i in f:
            tmp = i.split()
            start_index = int(tmp[0])
            num_of_end_points = int(tmp[1])
            for j in range(3, 3 + num_of_end_points):
                is_vertice[start_index-1] += 1
                line_x = []
                line_y = []
                line_z = []
                end_index = int(tmp[j])
                is_vertice[end_index-1] += 1
                line_x.append(x_axis[start_index - 1])
                line_y.append(y_axis[start_index - 1])
                line_z.append(z_axis[start_index - 1])
                line_x.append(x_axis[end_index - 1])
                line_y.append(y_axis[end_index - 1])
                line_z.append(z_axis[end_index - 1])
                ax.plot3D(line_x, line_y, line_z, 'gray')
        f.close()

        #ax.scatter3D(x_axis, y_axis, z_axis, 'blue', marker='o')

        if self.show_coord == True:
            for i in range(len(x_axis)):
                ax.text(x_axis[i], y_axis[i], z_axis[i],(x_axis[i], y_axis[i], z_axis[i]),fontsize = 6)
        plt.axis(self.axis_status)

        if self.show_pointnum == True:
            for i in range(len(x_axis)):
                ax.text(x_axis[i], y_axis[i], z_axis[i], i, fontsize=6)

        vertice_true = []
        vertice_false =[]

        for i in range(len(is_vertice)):
            if is_vertice[i]>=2:
                vertice_true.append(i)
            else:
                vertice_false.append(i)

        if len(vertice_false) == 0:
            self.vertices_analysis.setText('All points are vertices')
        elif len(vertice_false) == 1:
            the_point = vertice_false[0]
            the_coord = (x_axis[the_point], y_axis[the_point], z_axis[the_point])
            self.vertices_analysis.setText('This point is not a vertice: ' + str(the_point) + ' ' + str(the_coord))
        else:
            the_string = 'These points are not vertices: \n'
            for i in vertice_false:
                the_string += str(i) + ' ' + str((x_axis[i], y_axis[i], z_axis[i])) + '\n'
            self.vertices_analysis.setText(the_string)


        ax.scatter3D(x_axis, y_axis, z_axis, 'blue', marker='.')
        x = []
        y = []
        z = []

        for i in vertice_false:
            x.append(x_axis[i])
            y.append(y_axis[i])
            z.append(z_axis[i])
        ax.scatter3D(x,y,z, 'red', marker='*')
        self.plotting.draw()

    def diameter(self):
        pass

    def permutate(self):
        pass

    def changeValue(self):
        pass

    def shortestPath(self):
        pass

    def startover(self):
        pass

    def axis_off(self):
        self.axis_status = 'off'
        self.plot()
    def axis_on(self):
        self.axis_status = 'on'
        self.plot()
    def coord_off(self):
        self.show_coord = False
        self.plot()

    def coord_on(self):
        self.show_coord = True
        self.plot()
    def pointnum_off(self):
        self.show_pointnum = False
        self.plot()

    def pointnum_on(self):
        self.show_pointnum = True
        self.plot()



class NavigationToolbar(NavigationToolbar):
    # only display the buttons we need
    NavigationToolbar.toolitems = (
        ('Home', 'Reset original view', 'home', 'home'),
        ('Back', 'Back to previous view', 'back', 'back'),
        ('Forward', 'Forward to next view', 'forward', 'forward'),
        (None, None, None, None),
        ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
        ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
        # ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
        (None, None, None, None),
        # ('Save', 'Save the figure', 'filesave', 'save_figure'),
    )

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Window()
    sys.exit(app.exec_())