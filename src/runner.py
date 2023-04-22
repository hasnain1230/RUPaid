from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QApplication
from employeeController import EmployeeMainController
from employerController import EmployerMainController
import sys

from src.main import LoginPage


class Controller:
    def __init__(self, type='employee'):
        self.app = QtWidgets.QApplication(sys.argv)
        if type == 'employer':
            self.view = EmployerMainController()
        elif type == 'employee':
            self.view = EmployeeMainController()
        else:
            return

    def run(self):
        self.view.show()
        return self.app.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())

