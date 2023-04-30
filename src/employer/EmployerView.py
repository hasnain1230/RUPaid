import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, \
    QAbstractItemView
from PyQt5.QtGui import QFontDatabase


class EmployerView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.setMinimumSize(1100, 440)
        self.controller = controller
        self.setWindowTitle("RUPaid - Employer")
        self.database = self.controller.db_connection
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.controller.logout(timer=self.timer)) # TODO: Create the function for this
        self.timer.start(300000)
        self.installEventFilter(self)

        layout = QtWidgets.QVBoxLayout()

        # Set layout margin and spacing
        layout.setContentsMargins(20, 20, 20, 20)  # Adjust margins
        layout.setSpacing(20)

        title_layout = QtWidgets.QGridLayout()

        # Create a title for the window
        self.title = QtWidgets.QLabel(self)
        font = QFontDatabase.systemFont(QFontDatabase.TitleFont)  # Use QFontDatabase to find a suitable font
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setText(f"Welcome {self.controller.first_name} {self.controller.last_name}!")

        # Add the title to the title layout
        title_layout.addWidget(self.title, 0, 0, alignment=QtCore.Qt.AlignLeft)

        # Make the two buttons right next to each other
        title_layout.setColumnStretch(0, 1)
        title_layout.setColumnStretch(1, 0)
        title_layout.setColumnStretch(2, 0)

        layout.addLayout(title_layout, stretch=1)

        # Add a gray dividing line
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        divider.setStyleSheet("background-color: gray; height: 1px;")
        layout.addWidget(divider, alignment=QtCore.Qt.AlignTop, stretch=1)

        # Add a table for the employees
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["First Name", "Last Name", "Email", "Phone Number"])
        self.table.setRowCount(2)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectItems)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setStyleSheet("QTableWidget::item { padding: 10px; }")

        self.table.setItem(0, 0, QTableWidgetItem("John"))
        self.table.setItem(0, 1, QTableWidgetItem("Doe"))
        self.table.setItem(0, 2, QTableWidgetItem("Something"))
        self.table.setItem(0, 3, QTableWidgetItem("Something else"))

        self.table.setItem(1, 0, QTableWidgetItem("John"))
        self.table.setItem(1, 1, QTableWidgetItem("Doe"))
        self.table.setItem(1, 2, QTableWidgetItem("Something"))
        self.table.setItem(1, 3, QTableWidgetItem("Something else"))


        layout.addWidget(self.table, stretch=10)



        self.setLayout(layout)



    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a1.type() == QtCore.QEvent.MouseMove:
            print("Mouse moved")
            # Restart timer
            self.timer.stop()
            self.timer.start(300000)
            print(self.timer.remainingTime())

        return super().eventFilter(a0, a1)



