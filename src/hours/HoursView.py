from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QTableWidgetItem


class HoursView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.setFixedSize(800, 600)

        self.controller = controller
        self.setWindowTitle("RUPaid - Hours")
        self.timer = QtCore.QTimer()

        layout = QtWidgets.QVBoxLayout()

        # Set layout margin and spacing
        layout.setContentsMargins(20, 20, 20, 20)  # Adjust margins
        layout.setSpacing(20)

        self.hoursTable = QtWidgets.QTableWidget()
        self.hoursTable.setRowCount(7)
        self.hoursTable.setColumnCount(7)
        self.hoursTable.setColumnWidth(0, 108)
        self.hoursTable.setColumnWidth(1, 108)
        self.hoursTable.setColumnWidth(2, 108)
        self.hoursTable.setColumnWidth(3, 108)
        self.hoursTable.setColumnWidth(4, 108)
        self.hoursTable.setColumnWidth(5, 108)
        self.hoursTable.setColumnWidth(6, 110)
        self.hoursTable.verticalHeader().setVisible(False)
        self.hoursTable.horizontalHeader().setVisible(False)
        self.hoursTable.setItem(0, 0, QTableWidgetItem("Monday"))
        self.hoursTable.setItem(0, 1, QTableWidgetItem("Tuesday"))
        self.hoursTable.setItem(0, 2, QTableWidgetItem("Wednesday"))
        self.hoursTable.setItem(0, 3, QTableWidgetItem("Thursday"))
        self.hoursTable.setItem(0, 4, QTableWidgetItem("Friday"))
        self.hoursTable.setItem(0, 5, QTableWidgetItem("Saturday"))
        self.hoursTable.setItem(0, 6, QTableWidgetItem("Sunday"))
        layout.addWidget(self.hoursTable)

        # Add a gray dividing line
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        divider.setStyleSheet("background-color: gray; height: 1px;")
        self.setLayout(layout)
