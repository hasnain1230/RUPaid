from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from employeeController import EmployeeMainController
from employerController import EmployerMainController
import sys

class Controller:
    def __init__(self, type='employer'):
        self.app = QtWidgets.QApplication(sys.argv)
        if(type=='employer'):
            self.view = EmployerMainController()
        elif(type=='employee'):
            self.view = EmployeeMainController()
        else:
            return
    
    def run(self):
        self.view.show()
        return self.app.exec_()

if __name__ == '__main__':
    c = Controller()
    sys.exit(c.run())