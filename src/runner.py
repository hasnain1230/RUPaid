from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QApplication
from EmployeeController import EmployeeController

import sys

from src.Login import LoginPage


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())

