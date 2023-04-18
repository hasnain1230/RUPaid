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
        cursor = self.dbConnection.selectNamesFromTable()
        cursor.fetchall()
        numRows = cursor.rowcount
        cursor = self.dbConnection.selectNamesFromTable()

        self.ui.tableWidget.setRowCount(numRows)
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Name'])
        self.ui.tableWidget.setColumnWidth(0, 200)
        
        index = 0 
        for employeeName in cursor:
            self.ui.tableWidget.setItem(index,0, QTableWidgetItem(f'{employeeName[1]},  {employeeName[0]}'))
            index += 1
        