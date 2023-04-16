from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from employerUI import Ui_MainWindow
import sys

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.populateEmployees()
        
    def populateEmployees(self):
        employees = [
            {'first': 'Alex', 'last': 'Harris'},
            {'first': 'Kevin', 'last': 'Mcdaniel'},
            {'first': 'Labron', 'last': 'James'},
            {'first': 'Mike', 'last': 'Brown'},
            {'first': 'Kobe', 'last': 'Bryant'},
        ]
        self.ui.tableWidget.setRowCount(len(employees))
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Name'])
        for i, employee in enumerate(employees):
            name = f'{employee["last"]},  {employee["first"]}'
            self.ui.tableWidget.setItem(i,0, QTableWidgetItem(name))

        
        

def create_app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
    
create_app()