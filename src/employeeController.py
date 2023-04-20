from PyQt5 import QtWidgets
from employeeView import Ui_MainWindow

from dbConnection import DBConnection

class EmployeeMainController(QtWidgets.QMainWindow):
    def __init__(self):
        super(EmployeeMainController, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, QtWidgets.QMainWindow())
        self.dbConnection = DBConnection()
