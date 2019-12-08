import math
import sys
import re
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog, QDialog, QPushButton, QMessageBox

from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath, QPolygon
from PyQt5 import QtWidgets, QtGui, QtCore, uic

from PyQt5.QtCore import Qt

from tryout import dijkstra


class Node():
    def __init__(self,x,y,h,w,val):
        self.x=x
        self.h=h
        self.y=y
        self.w=w
        self.val=val

class edges():
    def __init__(self,fromN,toN,x1,y1,x2,y2,weight):
        self.fromN=fromN
        self.toN=toN
        self.x1 = x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.weight= weight

class WindowGui(QWidget):

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.h = 0
        self.w = 0
        self.val=""
        self.NodeList ={}
        self.edges={}
        self.tempEdges={}
        smalAlph = "abcdefghijklmnopqrstuvwxyz"
        self.alph = smalAlph + smalAlph.upper()



        self.initUI()

    def warningMes(self,error):
        buttonReply = QMessageBox.question(self, 'Error', error,
                                           QMessageBox.Ok)

    def initUI(self):

        self.setGeometry(200, 200, 1200, 900)
        self.setWindowTitle('Event handler')
        self.show()

    def get_directed_arrow_points(self, x1, y1, x2, y2, d):

        # get point for head of arrow--
        v1 = x1 - x2  # x cooridinate for vector between points
        v2 = y1 - y2  # y coordinate for vicot between points

        # to get unit vector requires: u = v/|v|
        dom = math.sqrt(math.pow(v1, 2) + math.pow(v2, 2))  # = |v|

        new_x = v1 / dom  # unit vector x component
        new_y = v2 / dom  # unit vecotr y componenet

        point1 = (
        x2 + new_x * d, y2 + new_y * d)  # given node radius d, we want to multiply the unit vector by d to get a
        # vector length d in the direction of the original vector.  Add x2 and y2
        # so that the point is located on the actual edge

        # get point of another vertex of the triangle--
        p1x = x2 + new_x * d * 2  # get x value of a point along the edge that is twice as far along the edge as the given node radius d
        p1y = y2 + new_y * d * 2  # get y value of point

        # because we now want a unit vector perpendicular to the original edge
        v2 = x1 - p1x  # switch x and y vector values
        v1 = -(y1 - p1y)  # and negate a vector component

        # to get unit vector requires: u = v/|v|
        dom = math.sqrt(math.pow(v1, 2) + math.pow(v2, 2))  # = |v|

        new_x = v1 / dom  # get unit vector components
        new_y = v2 / dom

        point2 = (p1x + new_x * d / 2.0, p1y + new_y * d / 2.0)  # length from this point to edge is 1/2 radius of node

        # get point of final vertex of triangle--
        # because we want the other unit vector perpendicular to the original edge
        v1 = y1 - p1y  # switch x and y vector values
        v2 = -(x1 - p1x)  # negate the other vector component this time

        # to get unit vector requires: u = v/|v|
        dom = math.sqrt(math.pow(v1, 2) + math.pow(v2, 2))  # = |v|

        new_x = v1 / dom  # get unit vector
        new_y = v2 / dom

        point3 = (p1x + new_x * d / 2.0, p1y + new_y * d / 2.0)  # length from this point to edge is 1/2 radius of node

        return ([point1, point2, point3])  # return a list of the three points

    def paintEvent(self, event):
        #init painter from QPainter object
        painter = QPainter(self)
        path = QPainterPath()
        painter.begin(self)

        painter.setRenderHint(QPainter.Antialiasing)
        #choose pen color
        painter.setPen(QtCore.Qt.red)
        #choose brush color
        painter.setBrush(QtCore.Qt.red)

        # print edges between nodes if exists
        for x in self.edges.values():
            painter.drawLine(x.x1, x.y1, x.x2, x.y2)
            ###################################################################################################
            ################### DRAW THE ARROWS "THIS CODE IS FROM ANOTHER SOURCE" ############################

            point_array = self.get_directed_arrow_points(x.x1, x.y1, x.x2, x.y2, 20)  # get coordinates of arrow vertices


            points = [QtCore.QPointF(point_array[0][0], point_array[0][1]),
                      QtCore.QPointF(point_array[1][0], point_array[1][1]),
                      QtCore.QPointF(point_array[2][0], point_array[2][1])]  # create a list of QPointF
            arrow = QtGui.QPolygonF(points)  # create a triangle with the given points
            painter.drawPolygon(arrow)  # draw arrow

            ######################################################################################################
            ######################################################################################################

            # set pen color to green, and type solid
        painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
        # set fill color to red
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

         #init node with attributes
        node = Node(self.x,self.y,self.h,self.w,self.val)
        #add it to our dictionary
        self.NodeList[node.val]=node
        # paint our nodes
        for i in self.NodeList.values():
            painter.drawEllipse(i.x,i.y,i.h,i.w)
        # new painter for text
        txtPaint = QPainter(self)
        #set pen color for yellow
        txtPaint.setPen(QPen(Qt.yellow, 10, Qt.SolidLine))
        #paint text over nodes
        for i in self.NodeList.values():
            txtPaint.drawText(i.x+18,i.y+23,i.val)
        #change pen color to red
        txtPaint.setPen(QPen(Qt.black, 10, Qt.SolidLine))
        #to paint text on the middle of the edge
        for x in self.edges.values():


            point_array = self.get_directed_arrow_points(x.x1, x.y1, x.x2, x.y2, 20)
            xAxis = point_array[1][0]
            yAxis = point_array[1][1]-10
            xAxis = int(xAxis)
            yAxis= int(yAxis)
            txtPaint.drawText(xAxis,yAxis,x.weight)





    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
    # On mouse click event
    def mousePressEvent(self, e):
        #Show input dialog
        text, ok = QInputDialog.getText(self, 'Add new Node', 'Enter node name:')
        if ok:
            if str(text).strip()=="":
               self.warningMes("Node name must be filled")
            elif len(str(text).strip())>1 or str(text).strip() not in self.alph:
                self.warningMes("Node name must one character of alphabets")
            elif str(text).strip() in self.NodeList.keys():
                self.warningMes("Node already exists")
            else:
                # initialize Node attributes
             self.val=str(text)
             self.x = e.pos().x()
             self.y = e.pos().y()
             self.h = 40
             self.w = 40
            #update after finishing
             self.update()


    def drawEdge(self,node1,node2,x1,y1,x2,y2,weight):
        edg =edges(node1,node2,x1,y1,x2,y2,weight)
        self.edges[node1+node2]=edg
        self.update()
        pass


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(432, 780)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.firstNode = QtWidgets.QLineEdit(self.centralwidget)
        self.firstNode.setGeometry(QtCore.QRect(140, 30, 113, 21))
        self.firstNode.setObjectName("firstNode")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 30, 51, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 71, 16))
        self.label_2.setObjectName("label_2")
        self.secondNode = QtWidgets.QLineEdit(self.centralwidget)
        self.secondNode.setGeometry(QtCore.QRect(140, 90, 113, 21))
        self.secondNode.setObjectName("secondNode")
        self.AddEdge = QtWidgets.QPushButton(self.centralwidget)
        self.AddEdge.setGeometry(QtCore.QRect(300, 30, 101, 41))
        self.AddEdge.setObjectName("AddEdge")
        self.weight = QtWidgets.QLineEdit(self.centralwidget)
        self.weight.setGeometry(QtCore.QRect(140, 160, 113, 20))
        self.weight.setObjectName("weight")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 160, 111, 16))
        self.label_3.setObjectName("label_3")
        self.deleteEdge = QtWidgets.QPushButton(self.centralwidget)
        self.deleteEdge.setGeometry(QtCore.QRect(300, 90, 101, 41))
        self.deleteEdge.setObjectName("deleteEdge")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 220, 441, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.delName = QtWidgets.QLineEdit(self.centralwidget)
        self.delName.setGeometry(QtCore.QRect(150, 250, 113, 20))
        self.delName.setObjectName("delName")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 250, 71, 16))
        self.label_4.setObjectName("label_4")
        self.deleteNode = QtWidgets.QPushButton(self.centralwidget)
        self.deleteNode.setGeometry(QtCore.QRect(300, 240, 101, 41))
        self.deleteNode.setObjectName("deleteNode")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(-10, 300, 451, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 330, 71, 16))
        self.label_5.setObjectName("label_5")
        self.chngName = QtWidgets.QLineEdit(self.centralwidget)
        self.chngName.setGeometry(QtCore.QRect(150, 330, 113, 20))
        self.chngName.setObjectName("chngName")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 370, 61, 16))
        self.label_6.setObjectName("label_6")
        self.newName = QtWidgets.QLineEdit(self.centralwidget)
        self.newName.setGeometry(QtCore.QRect(150, 370, 113, 20))
        self.newName.setObjectName("newName")
        self.btnChange = QtWidgets.QPushButton(self.centralwidget)
        self.btnChange.setGeometry(QtCore.QRect(300, 340, 101, 41))
        self.btnChange.setObjectName("btnChange")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(0, 410, 431, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.modifyEdge = QtWidgets.QPushButton(self.centralwidget)
        self.modifyEdge.setGeometry(QtCore.QRect(300, 150, 101, 41))
        self.modifyEdge.setObjectName("modifyEdge")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(90, 540, 241, 131))
        self.pushButton.setObjectName("pushButton")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 430, 61, 16))
        self.label_7.setObjectName("label_7")
        self.fromNode = QtWidgets.QLineEdit(self.centralwidget)
        self.fromNode.setGeometry(QtCore.QRect(100, 430, 113, 20))
        self.fromNode.setObjectName("fromNode")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(10, 470, 47, 13))
        self.label_8.setObjectName("label_8")
        self.ToNode = QtWidgets.QLineEdit(self.centralwidget)
        self.ToNode.setGeometry(QtCore.QRect(100, 470, 113, 20))
        self.ToNode.setObjectName("ToNode")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "First Node"))
        self.label_2.setText(_translate("MainWindow", "Second Node"))
        self.AddEdge.setText(_translate("MainWindow", "Add Edge"))
        self.label_3.setText(_translate("MainWindow", "Weight/New weight"))
        self.deleteEdge.setText(_translate("MainWindow", "Delete Edge"))
        self.label_4.setText(_translate("MainWindow", "Node Name"))
        self.deleteNode.setText(_translate("MainWindow", "Delete Node"))
        self.label_5.setText(_translate("MainWindow", "Node Name"))
        self.label_6.setText(_translate("MainWindow", "New Name"))
        self.btnChange.setText(_translate("MainWindow", "Change Name"))
        self.modifyEdge.setText(_translate("MainWindow", "Modify Edge"))
        self.pushButton.setText(_translate("MainWindow", "Generate Shortest Path"))
        self.label_7.setText(_translate("MainWindow", "From Node:"))
        self.label_8.setText(_translate("MainWindow", "To Node"))
        self.pushButton.clicked.connect(self.GenClicked)
        self.AddEdge.clicked.connect(self.edgeAdd)
        self.deleteEdge.clicked.connect(self.edgDelete)
        self.modifyEdge.clicked.connect(self.changeWeight)
        self.deleteNode.clicked.connect(self.nodeDelete)
        self.btnChange.clicked.connect(self.nameChange)

    def nameChange(self):
        oldName = self.chngName.text()
        newName = self.newName.text()
        self.chngName.setText("")
        self.newName.setText("")
        if oldName.strip()=="" or newName.strip()=="":
            ex.warningMes("You must fill the fields")
        elif oldName.strip() not in ex.NodeList.keys():
            ex.warningMes("Node does Not Exist")
        elif newName.strip() in ex.NodeList.keys():
            ex.warningMes("Similar node already exists")
        else:
            ex.val=""
            ex.NodeList[oldName.strip()].val = newName.strip()
            ex.NodeList[newName.strip()]=ex.NodeList[oldName.strip()]
            del(ex.NodeList[oldName.strip()])
            ex.update()


    def nodeDelete(self):
        node = self.delName.text()
        self.delName.setText("")
        if node.strip() == "":
            ex.warningMes("You must fill the field")
        elif node.strip() not in ex.NodeList.keys():
            ex.warningMes("Node does not exist")
        else:
            ex.x=0
            ex.y=0
            ex.val=""
            ex.h=0
            ex.w=0
            del(ex.NodeList[node.strip()])

            for i in ex.NodeList.keys():
                if (node.strip()+i) in ex.edges.keys():
                    del(ex.edges[node.strip()+i])
                elif (i+node.strip()) in ex.edges.keys():
                    del(ex.edges[i+node.strip()])
        ex.update()


    def changeWeight(self):
        node1 = self.firstNode.text()
        node2 = self.secondNode.text()
        weight = self.weight.text()
        self.firstNode.setText("")
        self.secondNode.setText("")
        self.weight.setText("")

        if node1.strip() == "" or node2.strip() == "" or weight.strip() == "":
            ex.warningMes("all fields must be filled")
        elif node1 not in ex.NodeList.keys() or node2 not in ex.NodeList.keys():
            ex.warningMes("Node does not exists")
        elif (node1.strip() + node2.strip()) not in ex.edges.keys():
            ex.warningMes("Edge does not exist !")
        elif (node1.strip() + node2.strip()) in ex.edges.keys():
          ex.edges[node1.strip() + node2.strip()].weight=weight

        ex.update()

    def edgDelete(self):
        node1 = self.firstNode.text()
        node2 = self.secondNode.text()
        self.firstNode.setText("")
        self.secondNode.setText("")


        if node1.strip() == "" or node2.strip() == "" :
            ex.warningMes("All fields must be filled")
        elif node1 not in ex.NodeList.keys() or node2 not in ex.NodeList.keys():
            ex.warningMes("Node does not exists")
        elif (node1.strip() + node2.strip()) in ex.edges.keys() :
            del(ex.edges[node1.strip() + node2.strip()])

        ex.update()



    def GenClicked(self):
        allEdg=[]
        for ver in ex.edges.values():
            allEdg.append((ver.fromN,ver.toN,int(ver.weight)))
        srcNode = self.fromNode.text().strip()
        trgtNode= self.ToNode.text().strip()
        result = str(dijkstra(allEdg,srcNode,trgtNode))

        if result == "inf":
            ex.warningMes("Its not connected")
        else :
           c = []
           smalAlph = "abcdefghijklmnopqrstuvwxyz"
           alph = smalAlph + smalAlph.upper()
           for i in result:
               if i in alph:
                   c.append(i)
           ex.tempEdges=ex.edges
           temp={}
           c.reverse()
           print(c)
           for i in range(0,len(c)-1,1):
               for edg in ex.edges.values():
                   if edg.fromN==c[i] and edg.toN == c[i+1]:
                       temp[c[i]+c[i+1]]=edg
                       print(edg.weight)


           ex.edges=temp
           ex.update()

    def RepresentsNotInt(s):
        try:
            int(s)
            return False
        except ValueError:
            return True
    def edgeAdd(self):

        node1 = self.firstNode.text()
        node2 = self.secondNode.text()
        weight = self.weight.text()
        self.firstNode.setText("")
        self.secondNode.setText("")
        self.weight.setText("")


        if node1.strip()=="" or node2.strip()=="" or weight.strip()=="":
            ex.warningMes("All fields must be filled")
        elif not weight.strip().isdigit():
            ex.warningMes("Weight should be a positive  integer")
        elif node1 not in ex.NodeList.keys() or node2 not in ex.NodeList.keys():
            ex.warningMes(" There is a Node that does not exists")
        elif (node1.strip()+node2.strip()) in ex.edges.keys():
            ex.warningMes("Edge exists !")

        else:
            ex.drawEdge(node1,node2,ex.NodeList[node1].x+15,ex.NodeList[node1].y+15,ex.NodeList[node2].x+15,ex.NodeList[node2].y+15,weight)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WindowGui()
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
