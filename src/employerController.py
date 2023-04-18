from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from employerView import Ui_MainWindow
import sys

from dbConnection import DBConnection

class EmployerMainController(QtWidgets.QMainWindow):
    def __init__(self):
        super(EmployerMainController, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dbConnection = DBConnection()
        self.populateEmployees()

        
    def populateEmployees(self):
        cursor = self.dbConnection.selectFromTable()
        cursor.fetchall()
        numRows = cursor.rowcount
        cursor = self.dbConnection.selectFromTable()

        self.ui.tableWidget.setRowCount(numRows)
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Name', 'Age'])
        
        index = 0 
        for employee in cursor:
            name = employee[0]
            age = employee[1]
            self.ui.tableWidget.setItem(index,0, QTableWidgetItem(name))
            self.ui.tableWidget.setItem(index,1, QTableWidgetItem(str(age)))
            index += 1
        