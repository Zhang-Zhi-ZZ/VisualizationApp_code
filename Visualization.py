import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import os
import images
from mpl_toolkits.mplot3d import Axes3D
import pickle
import numpy as np
from math import *


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Visualize it!"
        # self.top = 100
        # self.left = 100
        # self.width = 600
        # self.height = 350
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.top, self.left, self.width, self.height)
        self.setFixedSize(600, 350)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(":McMaster.png")))
        self.setPalette(palette)

        App_logo = QLabel(self)
        App_logo.setGeometry(50, 80, 550, 250)
        App_logo.setObjectName("App_logo")
        logo = QtGui.QPixmap(":logo.png").scaled(550, 250)
        App_logo.setPixmap(logo)

        start = QPushButton(self)
        start.setStyleSheet("QPushButton{border-image: url(:start.png)}")
        start.setCursor(QCursor(Qt.PointingHandCursor))
        start.setGeometry(480, 250, 120, 110)
        start.clicked.connect(self.startApp_onClick)

        self.show()

    @pyqtSlot()
    def startApp_onClick(self):
        self.statusBar().showMessage("Switched to window 1")
        # self.cams = loadFile()
        self.cams = result()
        self.cams.show()
        self.close()


class result(QMainWindow):
    global x_axis, y_axis, z_axis
    global line_x, line_y, line_z
    global show_axis, axis_status
    global InputPoints, InputEdges

    def __init__(self, parent=None):
        super(result, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Plot')
        self.add_menubar()
        self.add_content()

    def add_menubar(self):
        mainMenu = self.menuBar()
        #fileMenu = mainMenu.addMenu('File')
        #fileMenu.addAction("New Plot")

        axis_off_action = QAction('Do not show axis', self)
        axis_off_action.triggered.connect(self.axis_off)
        axis_on_action = QAction('Show axis', self)
        axis_on_action.triggered.connect(self.axis_on)
        coord_off_action = QAction('Do not show point coordinates', self)
        coord_off_action.triggered.connect(self.coord_off)
        coord_on_action = QAction('Show point coordinates', self)
        coord_on_action.triggered.connect(self.coord_on)
        pointnum_off_action = QAction('Do not show point number', self)
        pointnum_off_action.triggered.connect(self.pointnum_off)
        pointnum_on_action = QAction('Show point number', self)
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


        permute_action = QAction('Permuate Variables', self)
        permute_action.triggered.connect(self.permutate)

        change_action = QAction('Change Variables', self)
        change_action.triggered.connect(self.changeValue)

        shortestPath_action = QAction('Shortest Path',self)
        shortestPath_action.triggered.connect(self.shortestPath)

        diameter_action = QAction('Diameter',self)
        diameter_action.triggered.connect(self.diameter)

        computeMenu = mainMenu.addMenu("Compute")
        computeMenu.addAction(diameter_action)
        computeMenu.addAction(shortestPath_action)
        #helpMenu = mainMenu.addMenu("Help")
        #helpMenu.addAction("Instructions")

    def add_content(self):
        # self.setWindowTitle('Plot')
        # self.setFixedSize(600,800)

        self.pointFileLabel = QLabel(self)
        self.pointFileLabel.setText('Please select the file containing your point data:')
        self.pointFileLabel.setStyleSheet("font: 10pt Helvetica")

        self.pointFile = QPushButton(self)
        self.pointFile.setStyleSheet('background-color: rgb(245,255,250); color: #2F4F4F; font: 8pt Helvetica')
        self.pointFile.setText('Open')
        self.pointFile.clicked.connect(self.OpenPointFile)
        # self.pointFile.setGeometry(320,100,50,20)
        self.pointFile.setCursor(QCursor(Qt.PointingHandCursor))

        self.label1 = QLabel(self)
        # self.label1.setGeometry(20, 120, 400, 40)
        # self.label1.setFixedWidth(400)
        # self.label1.setText('')
        self.label1.setWordWrap(True)
        self.label1.setStyleSheet("font: 9pt Helvetica; color: #C0C0C0")

        self.edgeFileLabel = QLabel(self)
        self.edgeFileLabel.setText('Please select the file containing your edge data: ')
        # self.edgeFileLabel.setGeometry(20,155,300,20)
        self.edgeFileLabel.setStyleSheet("font: 10pt Helvetica")

        self.label2 = QLabel(self)
        # self.label2.setGeometry(20, 170, 500, 40)
        # self.label2.setFixedWidth(400)
        self.label2.setWordWrap(True)
        # self.label2.setText('')
        self.label2.setStyleSheet("font: 9pt Helvetica; color: #C0C0C0")

        self.edgeFile = QPushButton(self)
        self.edgeFile.setStyleSheet('background-color: rgb(245,255,250); color: #2F4F4F; font: 8pt Helvetica')
        self.edgeFile.setText('Open')
        self.edgeFile.clicked.connect(self.OpenEdgeFile)
        # self.edgeFile.setGeometry(320, 150, 50, 20)
        self.edgeFile.setCursor(QCursor(Qt.PointingHandCursor))

        self.skip_edgeFile = QPushButton(self)
        self.skip_edgeFile.setStyleSheet('background-color: rgb(245,255,250); color: #2F4F4F; font: 8pt Helvetica')
        self.skip_edgeFile.setText('Skip')
        self.skip_edgeFile.clicked.connect(self.SkipOpenEdgeFile)
        # self.edgeFile.setGeometry(320, 150, 50, 20)
        self.skip_edgeFile.setCursor(QCursor(Qt.PointingHandCursor))

        self.plot_button = QPushButton(self)
        self.plot_button.setStyleSheet('background-color: rgb(255,0,0); color: #FFFFFF; font: 10pt Helvetica')
        self.plot_button.setText('Plot')
        self.plot_button.clicked.connect(self.start_plot)

        self.figure = plt.figure()
        self.figure.tight_layout()
        self.plotting = FigureCanvas(self.figure)
        self.plotting.resize(100, 100)
        self.plot_status = 'off'
        self.axis_status = 'on'
        self.show_coord = False
        self.show_pointnum = False

        self.vertices_analysis = QLabel(self)
        # self.vertices_analysis.setFixedSize(100,40)
        self.vertices_analysis.setWordWrap(True)

        self.shortestPath_label = QLabel(self)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(50)
        self.scroll.setWidget(self.vertices_analysis)

        self.toolbar = NavigationToolbar(self.plotting, self)
        # self.toolbar.setGeometry(20,10,200,20)

        horizontalLayout1 = QHBoxLayout()
        horizontalLayout1.addWidget(self.pointFileLabel)
        horizontalLayout1.addWidget(self.pointFile)

        horizontalLayout2 = QHBoxLayout()
        horizontalLayout2.addWidget(self.edgeFileLabel)
        horizontalLayout2.addWidget(self.edgeFile)
        horizontalLayout2.addWidget(self.skip_edgeFile)

        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(self.toolbar)
        verticalLayout.addLayout(horizontalLayout1)
        verticalLayout.addWidget(self.label1)
        verticalLayout.addLayout(horizontalLayout2)
        verticalLayout.addWidget(self.label2)
        verticalLayout.addWidget(self.plot_button)
        verticalLayout.addWidget(self.plotting)
        verticalLayout.addWidget(self.shortestPath_label)
        verticalLayout.addWidget(self.scroll)
        # verticalLayout.addWidget(self.vertices_analysis)

        # self.setLayout(verticalLayout)

        layout_widget = QWidget()
        layout_widget.setLayout(verticalLayout)
        self.setCentralWidget(layout_widget)
        # self.setGeometry(300, 300, 350, 300)
        # self.setWindowTitle('Plot')
        # self.show()

    def OpenPointFile(self):
        # output： C:/Users/ZZ/PycharmProject/.../InputPoints.txt
        global InputPoints, InputEdges
        InputPoints = str(QFileDialog().getOpenFileName(None, "Open file", "", "Text Files (*.txt)")[0])
        self.label1.setText('Selected file: ' + InputPoints)
        self.plot_status = 'on'
        InputEdges = ''

    def OpenEdgeFile(self):
        global InputEdges
        # output： C:/Users/ZZ/PycharmProject/.../InputPoints.txt
        InputEdges = str(QFileDialog().getOpenFileName(None, "Open file", "", "Text Files (*.txt)")[0])
        self.label2.setText('selected file: ' + InputEdges)

    def SkipOpenEdgeFile(self):
        self.label2.setText('No edge file')

    def start_plot(self):
        if self.plot_status == 'on':
            self.data()
            self.plot()

    def data(self):
        global is_vertice, x_axis, y_axis, z_axis, line_x, line_y, line_z
        global point_dict, edge_dict
        global is_vertice
        global the_path
        the_path = []
        file_path = os.path.realpath(InputPoints)

        point_dict, edge_dict = {}, {}
        x_axis = []
        y_axis = []
        z_axis = []
        num = 1
        with open(file_path) as f:
            for i in f:
                tmp = i.split()
                point_dict[num] = [int(tmp[0]), int(tmp[1]), int(tmp[1])]
                x_axis.append(int(tmp[0]))
                y_axis.append(int(tmp[1]))
                z_axis.append(int(tmp[2]))
            f.close()

        if InputEdges != '':
            f = open(InputEdges, "r")
            for i in f:
                tmp = i.split()
                start_index = int(tmp[0])
                # num_of_end_points = int(tmp[1])
                edge_dict[start_index] = tmp[3:]
            f.close()

        x_axis.append(0)
        y_axis.append(0)
        z_axis.append(0)

        x_axis.append(10)
        y_axis.append(10)
        z_axis.append(10)

        is_vertice = [0 for i in range(len(x_axis))]

    def plot(self):
        global vertice_true,shortest_distance
        shortest_distance = float('inf')
        longest_path = []
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')

        if InputEdges != '':
            for start, ends in edge_dict.items():
                for e in ends:
                    is_vertice[start - 1] += 1
                    is_vertice[int(e) - 1] += 1
                    line_x = []
                    line_y = []
                    line_z = []
                    line_x.append(x_axis[start - 1])
                    line_y.append(y_axis[start - 1])
                    line_z.append(z_axis[start - 1])
                    line_x.append(x_axis[int(e) - 1])
                    line_y.append(y_axis[int(e) - 1])
                    line_z.append(z_axis[int(e) - 1])
                    ax.plot3D(line_x, line_y, line_z, 'gray')

        edge_x = []
        edge_y = []
        edge_z = []
        if the_path != '':
            for i in range(len(the_path)-1):
                j = int(the_path[i])
                k = int(the_path[i+1])
                edge_x.append(x_axis[j])
                edge_y.append(y_axis[j])
                edge_z.append(z_axis[j])
                edge_x.append(x_axis[k])
                edge_y.append(y_axis[k])
                edge_z.append(z_axis[k])
                ax.plot3D(edge_x, edge_y, edge_z, 'red')
        if self.show_coord == True:
            for i in range(len(x_axis)):
                ax.text(x_axis[i], y_axis[i], z_axis[i], (x_axis[i], y_axis[i], z_axis[i]), fontsize=6)
        plt.axis(self.axis_status)

        if self.show_pointnum == True:
            for i in range(len(x_axis)):
                ax.text(x_axis[i], y_axis[i], z_axis[i], i + 1, fontsize=6)

        vertice_true = []
        vertice_false = []

        for i in range(len(is_vertice)):
            if is_vertice[i] >= 2:
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

        x = []
        y = []
        z = []
        for i in vertice_true:
            x.append(x_axis[i])
            y.append(y_axis[i])
            z.append(z_axis[i])
        ax.scatter3D(x, y, z, 'blue', marker='.')

        x2 = []
        y2 = []
        z2 = []

        for i in vertice_false:
            x2.append(x_axis[i])
            y2.append(y_axis[i])
            z2.append(z_axis[i])
        ax.scatter3D(x2, y2, z2, 'red', marker='*')
        self.plotting.draw()

    def permutate(self):
        global axis_rows
        # add the tabel showing input points data
        self.tabel_widget = QTableWidget()
        num_of_points = len(x_axis)
        self.tabel_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabel_widget.setFixedSize(350, 400)
        self.tabel_widget.setRowCount(num_of_points)
        self.tabel_widget.setColumnCount(3)
        self.tabel_widget.setHorizontalHeaderLabels(['x', 'y', 'z'])
        for i in range(num_of_points):
            newItem = QTableWidgetItem(str(x_axis[i]))
            self.tabel_widget.setItem(i, 0, newItem)
            newItem = QTableWidgetItem(str(y_axis[i]))
            self.tabel_widget.setItem(i, 1, newItem)
            newItem = QTableWidgetItem(str(z_axis[i]))
            self.tabel_widget.setItem(i, 2, newItem)

        axis_label = QLabel('Axis')
        axis = 'x'
        axis_list = ['y', 'z']
        point1 = '1'
        point2 = '1'
        point_list = [str(i + 1) for i in range(1, num_of_points)]

        row1_label = QLabel('Row 1')
        row2_label = QLabel('Row 2')

        self.choose_axis = QComboBox()
        self.choose_axis.addItem(axis)
        self.choose_axis.addItems(axis_list)
        self.choose_axis.currentIndexChanged.connect(lambda: self.on_combobox_func(self.choose_axis))

        self.row1 = QComboBox()
        self.row1.addItem(point1)
        self.row1.addItems(point_list)
        self.row1.currentIndexChanged.connect(lambda: self.on_combobox_func(self.row1))

        self.row2 = QComboBox()
        self.row2.addItem(point2)
        self.row2.addItems(point_list)
        self.row2.currentIndexChanged.connect(lambda: self.on_combobox_func(self.row2))

        self.plot_button = QPushButton(self)
        self.plot_button.setStyleSheet('background-color: rgb(255,0,0); color: #FFFFFF; font: 10pt Helvetica')
        self.plot_button.setText('Permutate and Plot')
        self.plot_button.clicked.connect(self.exchangeRow)

        axis_rows = [self.choose_axis.currentText(), self.row1.currentText(), self.row2.currentText()]
        self.pwindow = QWidget()

        layout1 = QHBoxLayout()
        layout1.addWidget(axis_label)
        layout1.addWidget(self.choose_axis)

        layout2 = QHBoxLayout()
        layout2.addWidget(row1_label)
        layout2.addWidget(self.row1)

        layout3 = QHBoxLayout()
        layout3.addWidget(row2_label)
        layout3.addWidget(self.row2)

        layout = QVBoxLayout()
        self.pwindow.setLayout(layout)
        layout.addWidget(self.tabel_widget)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addWidget(self.plot_button)
        self.pwindow.setWindowTitle('Permutate Variables')
        self.pwindow.show()

    def on_combobox_func(self, combobox):
        if combobox == self.choose_axis:
            axis_rows[0] = combobox.currentText()
        elif combobox == self.row1:
            axis_rows[1] = combobox.currentText()
        else:
            axis_rows[2] = combobox.currentText()

    def exchangeRow(self):
        row1 = int(axis_rows[1])
        row2 = int(axis_rows[2])
        if axis_rows[0] == 'x':
            x_axis[row1 - 1], x_axis[row2 - 1] = x_axis[row2 - 1], x_axis[row1 - 1]
        elif axis_rows[0] == 'y':
            y_axis[row1 - 1], y_axis[row2 - 1] = y_axis[row2 - 1], y_axis[row1 - 1]
        else:
            z_axis[row1 - 1], z_axis[row2 - 1] = z_axis[row2 - 1], z_axis[row1 - 1]
        self.new_plot()

    def new_plot(self):
        self.pwindow.close()
        self.plot()
        if shortest_distance != float('inf'):
            self.shortestPath_label.setText(
                'The Shortest Distance From Point {} to Point {} is {}'.format(path_vertice[0], path_vertice[1], shortest_distance))

    def changeValue(self):
        # add the tabel showing input points data
        self.tabel_widget = QTableWidget()
        num_of_points = len(x_axis)
        self.tabel_widget.setFixedSize(350, 500)
        self.tabel_widget.setRowCount(num_of_points)
        self.tabel_widget.setColumnCount(3)
        self.tabel_widget.setHorizontalHeaderLabels(['x', 'y', 'z'])
        for i in range(num_of_points):
            newItem = QTableWidgetItem(str(x_axis[i]))
            self.tabel_widget.setItem(i, 0, newItem)
            newItem = QTableWidgetItem(str(y_axis[i]))
            self.tabel_widget.setItem(i, 1, newItem)
            newItem = QTableWidgetItem(str(z_axis[i]))
            self.tabel_widget.setItem(i, 2, newItem)
        self.tabel_widget.cellChanged.connect(self.cell)

        self.intro_label = QLabel()
        self.intro_label.setStyleSheet('font: 15pt Helvetica')
        self.intro_label.setText('Double click on the cell to edit the value.')

        self.plot_button = QPushButton(self)
        self.plot_button.setStyleSheet('background-color: rgb(255,0,0); color: #FFFFFF; font: 10pt Helvetica')
        self.plot_button.setText('Confirm and Plot')
        self.plot_button.clicked.connect(self.new_plot)

        self.pwindow = QWidget()

        layout = QVBoxLayout()
        self.pwindow.setLayout(layout)
        layout.addWidget(self.intro_label)
        layout.addWidget(self.tabel_widget)
        layout.addWidget(self.plot_button)
        self.pwindow.setWindowTitle('Change Variable Values')
        self.pwindow.show()

    def cell(self):
        new = self.tabel_widget.currentItem()
        new_value = int(new.text())

        point = self.tabel_widget.currentRow()
        axis = self.tabel_widget.currentColumn()

        if axis == 0:
            x_axis[point] = new_value
        elif axis == 1:
            y_axis[point] = new_value
        else:
            z_axis[point] = new_value

    def Dijkstra(self, Vertex, EndNode):
        global num_vertex, graph
        num_vertex = len(edge_dict)
        graph = np.full((num_vertex, num_vertex), float('inf'))
        for start, ends in edge_dict.items():
            start_x = x_axis[start-1]
            start_y = y_axis[start-1]
            start_z = z_axis[start-1]
            graph[start-1, start-1] = 0
            for e in ends:
                end_x = x_axis[int(e)-1]
                end_y = y_axis[int(e)-1]
                end_z = z_axis[int(e)-1]
                dist = sqrt((start_x - end_x) ** 2 + (start_y - end_y) ** 2 + (start_z - end_z) ** 2)
                graph[start-1, int(e)-1] = dist
        Dist = [[] for i in range(num_vertex)]  # 存储源点到每一个终点的最短路径的长度
        Path = [[] for i in range(num_vertex)]  # 存储每一条最短路径中倒数第二个顶点的下标
        flag = [[] for i in range(num_vertex)]  # 记录每一个顶点是否求得最短路径
        index = 0
        # initialize
        while index < num_vertex:
            Dist[index] = graph[Vertex][index]
            flag[index] = 0
            if graph[Vertex][index] < float('inf'):
                Path[index] = Vertex
            else:
                Path[index] = -1 #表示从顶点Vertex到index无路径
            index += 1
        flag[Vertex] = 1
        Path[Vertex] = 0
        Dist[Vertex] = 0
        index = 1

        while index < num_vertex:
            MinDist = float('inf')
            j = 0
            while j < num_vertex:
                if flag[j] == 0 and Dist[j] < MinDist:
                    tVertex = j  # tVertex为目前从V-S集合中找出的距离源点Vertex最断路径的顶点
                    MinDist = Dist[j]
                j += 1
            flag[tVertex] = 1
            EndVertex = 0
            MinDist = float('inf')  # 表示无穷大，若两点间的距离小于MinDist说明两点间有路径
            while EndVertex < num_vertex:
                if flag[EndVertex] == 0:
                    if graph[tVertex][EndVertex] < MinDist and \
                            Dist[tVertex] + graph[tVertex][EndVertex] < Dist[EndVertex]:
                        Dist[EndVertex] = Dist[tVertex] + graph[tVertex][EndVertex]
                        Path[EndVertex] = tVertex
                EndVertex += 1
            index += 1
        vertex_endnode_path = []
        return Dist[EndNode], self.start_end_path(Path, Vertex, EndNode, vertex_endnode_path)

    def start_end_path(self, Path, start, endnode, path):
        if start == endnode:
            path.append(start)
        else:
            path.append(endnode)
            self.start_end_path(Path, start, Path[endnode], path)
        print(path)
        return path


    def shortestPath(self):
        global path_vertice
        self.tabel_widget = QTableWidget()
        num_of_points = len(x_axis)
        self.tabel_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabel_widget.setFixedSize(350, 400)
        self.tabel_widget.setRowCount(num_of_points)
        self.tabel_widget.setColumnCount(3)
        self.tabel_widget.setHorizontalHeaderLabels(['x', 'y', 'z'])
        for i in range(num_of_points):
            newItem = QTableWidgetItem(str(x_axis[i]))
            self.tabel_widget.setItem(i, 0, newItem)
            newItem = QTableWidgetItem(str(y_axis[i]))
            self.tabel_widget.setItem(i, 1, newItem)
            newItem = QTableWidgetItem(str(z_axis[i]))
            self.tabel_widget.setItem(i, 2, newItem)


        point1 = '1'
        point2 = '1'
        point_list = [str(i + 1) for i in range(1, num_of_points)]

        row1_label = QLabel('Start Point')
        row2_label = QLabel('End Point')


        self.start_point = QComboBox()
        self.start_point.addItem(point1)
        self.start_point.addItems(point_list)
        self.start_point.currentIndexChanged.connect(lambda: self.on_combobox_func_path(self.start_point))

        self.end_point = QComboBox()
        self.end_point.addItem(point2)
        self.end_point.addItems(point_list)
        self.end_point.currentIndexChanged.connect(lambda: self.on_combobox_func_path(self.end_point))

        self.plot_button = QPushButton(self)
        self.plot_button.setStyleSheet('background-color: rgb(255,0,0); color: #FFFFFF; font: 10pt Helvetica')
        self.plot_button.setText('Calculate and Plot')
        self.plot_button.clicked.connect(self.plot_path)

        path_vertice = [self.start_point.currentText(),self.end_point.currentText()]

        self.pwindow = QWidget()

        layout2 = QHBoxLayout()
        layout2.addWidget(row1_label)
        layout2.addWidget(self.start_point)

        layout3 = QHBoxLayout()
        layout3.addWidget(row2_label)
        layout3.addWidget(self.end_point)

        layout = QVBoxLayout()
        self.pwindow.setLayout(layout)
        layout.addWidget(self.tabel_widget)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addWidget(self.plot_button)
        self.pwindow.setWindowTitle('Calculate Shortest Path')
        self.pwindow.show()

    def on_combobox_func_path(self, combobox):
        if combobox == self.start_point:
            path_vertice[0] = combobox.currentText()
        else:
            path_vertice[1] = combobox.currentText()

    def plot_path(self):
        global shortest_distance, the_path
        start = int(path_vertice[0])-1
        end = int(path_vertice[1])-1
        shortest_distance = float('inf')
        shortest_distance, the_path = self.Dijkstra(start, end)
        self.new_plot()

    def find_diameter(self):
        global the_diameter, longest_path
        current_longest_path = 0
        vertex_num = len(vertice_true )
        for i in range(vertex_num):
            for j in range(i,vertex_num):
                dist,path = self.Dijkstra(i,j)
                if dist > current_longest_path and dist!= float('inf'):
                    current_longest_path = dist
                    longest_path = path
        the_diameter = current_longest_path
    def diameter(self):
        self.find_diameter()
        self.pwindow = QWidget()

        self.diameter_label = QLabel(self)
        self.diameter_label.setText('The diameter is: {}'.format(the_diameter))
        self.diameter_label.setAlignment(Qt.AlignCenter)

        self.show_diameter_button = QPushButton(self)
        self.show_diameter_button.setText('Show the diameter')
        self.show_diameter_button.clicked.connect(self.show_diameter)

        layout = QVBoxLayout()
        self.pwindow.setLayout(layout)
        layout.addWidget(self.diameter_label)
        layout.addWidget(self.show_diameter_button)
        self.pwindow.setWindowTitle('Diameter')
        self.pwindow.show()

    def show_diameter(self):
        global the_path
        the_path = longest_path
        self.new_plot()

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
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
