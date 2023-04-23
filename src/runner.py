from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QApplication
from employeeController import EmployeeMainController
from employerController import EmployerMainController
import sys

from main import LoginPage


app = QApplication(sys.argv)
login_page = LoginPage()
login_page.show()
sys.exit(app.exec_())

