from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from employerController import EmployerMainController
import sys

class Controller:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.view = EmployerMainController()

    def run(self):
        self.view.show()
        return self.app.exec_()

    
    

if __name__ == '__main__':
    c = Controller()
    sys.exit(c.run())