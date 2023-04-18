from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from employerView import Ui_MainWindow
import sys

from dbConnection import DBConnection

class EmployerMainController(QtWidgets.QMainWindow):
    def __init__(self):
        super(EmployerMainController, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, QtWidgets.QMainWindow())
        self.dbConnection = DBConnection()

        
    
        