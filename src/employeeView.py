# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'employer1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from dbConnection import DBConnection

from employee import Employee

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, source):
        MainWindow.setObjectName("RUPaid - Employee")
        MainWindow.resize(1068, 680)
        self.win1 = MainWindow
        source.close()
        self.dbConnection = DBConnection()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 171, 31))
        self.label.setObjectName("label")
        
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(170, 20, 231, 22))
        self.lineEdit.setPlaceholderText("Search for Employee")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(570, 60, 481, 411))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget,clicked = lambda: self.logout())
        self.pushButton.setGeometry(QtCore.QRect(980, 10, 81, 26))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.viewPay())
        self.pushButton_3.setGeometry(QtCore.QRect(570, 490, 231, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.viewProfile())
        self.pushButton_4.setGeometry(QtCore.QRect(810, 490, 231, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.viewHours())
        self.pushButton_5.setGeometry(QtCore.QRect(570, 560, 231, 51))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.viewNotif())
        self.pushButton_6.setGeometry(QtCore.QRect(810, 560, 231, 51))
        self.pushButton_6.setObjectName("pushButton_6")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1068, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RUPaid - Employee"))
        self.label.setText(_translate("MainWindow", "Welcome,  User!"))
        self.pushButton.setText(_translate("MainWindow", "Log Out"))
        self.pushButton_3.setText(_translate("MainWindow", "View Pay"))
        self.pushButton_4.setText(_translate("MainWindow", "Edit Profile"))
        self.pushButton_5.setText(_translate("MainWindow", "View Hours"))
        self.pushButton_6.setText(_translate("MainWindow", "View Notifications"))
    
    def viewNotif(self):
        return
    
    def viewProfile(self):
        #employee = self.getSelectedEmployee()
        #self.win = QtWidgets.QMainWindow()
        #from employeeProfileWindow import Ui_EmployeeProfileWindow
        #self.ui = Ui_EmployeeProfileWindow()
        #self.ui.setupUi(self.win, self.win1, employee)
        #self.win.show()
        return
    
    def logout(self):
        return
    
    def viewPay(self):
        return
    
    def viewHours(self):
        return
    