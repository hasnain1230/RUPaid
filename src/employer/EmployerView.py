from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QTableWidget, \
    QAbstractItemView
from PyQt5.QtGui import QFontDatabase
from src.employer.AddUserWindow import AddUser
from src.RUPaid.ChangePasswordWindow import ChangePasswordWindow

SELECTED_ROW_CONSTANT = 10


class EmployerView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.setMinimumSize(1500, 440)
        self.controller = controller
        self.setWindowTitle("RUPaid - Employer")
        self.database = self.controller.db_connection
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(
            lambda: self.controller.logout(timer=self.timer), )  # TODO: Create the function for this
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

        logout_button = QtWidgets.QPushButton("Logout")
        logout_button.clicked.connect(lambda: self.controller.logout(timer=self.timer))
        logout_button.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 5px;")
        title_layout.addWidget(logout_button, 0, 1, alignment=QtCore.Qt.AlignRight)

        layout.addLayout(title_layout, stretch=1)

        # Add a gray dividing line
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        divider.setStyleSheet("background-color: gray; height: 1px;")
        layout.addWidget(divider, alignment=QtCore.Qt.AlignTop, stretch=1)

        self.table_labels = [
            ["User ID", "user_id"],
            ["Username", "user_name"],
            ["First Name", "first_name"],
            ["Last Name", "last_name"],
            ["Role", "role"],
            ["Age", "age"],
            ["Occupation", "occupation"],
            ["Hourly Pay", "hourly_pay"],
            ["Email Address", "email"],
            ["Bank Account Number", "bankAccountNumber"],
            ["Routing Number", "bankRoutingNumber"]
        ]

        # Add a table for the employees
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.table_labels))
        self.table.setHorizontalHeaderLabels([label[0] for label in self.table_labels])
        self.table.doubleClicked.connect(lambda: self.edit_user())
        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)

        # Install event listener when field is edited
        self.table.itemChanged.connect(self.item_changed)
        self.table.itemSelectionChanged.connect(self.prepare_buttons)
        # Allow columns to be resized
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.table.setStyleSheet("QTableWidget::item { padding: 10px; }")
        self.populate_table()
        layout.addWidget(self.table, stretch=10)

        button_layout = QtWidgets.QHBoxLayout()

        button_layout.addStretch(1)

        # Change Password
        self.change_password_button = QtWidgets.QPushButton("Change Password")
        self.change_password_button.clicked.connect(lambda: self.change_password())
        self.change_password_button.setDisabled(True)
        button_layout.addWidget(self.change_password_button, alignment=QtCore.Qt.AlignRight)

        # Refresh Button
        refresh_button = QtWidgets.QPushButton("Refresh")
        refresh_button.clicked.connect(lambda: self.populate_table())
        button_layout.addWidget(refresh_button, alignment=QtCore.Qt.AlignRight)

        # Add user button
        add_user_button = QtWidgets.QPushButton("Add User")
        # Add user function and populate table again
        add_user_button.clicked.connect(lambda: self.add_user())
        button_layout.addWidget(add_user_button, alignment=QtCore.Qt.AlignRight)

        # Remove user button
        self.remove_user_button = QtWidgets.QPushButton("Remove User")
        self.remove_user_button.setDisabled(True)
        self.remove_user_button.clicked.connect(lambda: self.remove_user())
        button_layout.addWidget(self.remove_user_button, alignment=QtCore.Qt.AlignRight)

        # Make it so that the buttons are right next to each other on the right side of the window

        layout.addLayout(button_layout, stretch=0)

        self.setLayout(layout)

    def add_user(self):
        # Add a new row to the table
        self.table.insertRow(self.table.rowCount())
        # Fill row with default values
        self.table.setItem(self.table.rowCount() - 1, 0,
                           QtWidgets.QTableWidgetItem(f"{self.controller.get_next_user_id()}"))

        new_user = AddUser(self.controller.get_next_user_id, self.controller, self.populate_table)
        new_user.show()

    def item_changed(self, item):
        # Get the row and column of the item that was changed
        row = item.row()
        column = item.column()

        # Find the column name from the table labels
        column_name = self.table_labels[column][1]

        # Get the value of the item
        value = item.text()

        # Get the user id of the user that was changed
        user_id = self.table.item(row, 0).text()

        # Update the user in the database
        self.controller.update_user(user_id, column_name, value)

    def change_password(self):
        change_password = ChangePasswordWindow(self.controller)
        change_password.show()

    def prepare_buttons(self):
        selected_row = self.table.selectedIndexes()

        if len(selected_row) == SELECTED_ROW_CONSTANT:
            self.change_password_button.setDisabled(False)
        else:
            self.change_password_button.setDisabled(True)

        if len(selected_row) != 0 and len(selected_row) % SELECTED_ROW_CONSTANT == 0:
            self.remove_user_button.setDisabled(False)
        else:
            self.remove_user_button.setDisabled(True)

    def edit_user(self):
        pass

    def populate_table(self):
        users = self.controller.get_all_users()
        # * out all but last 4 digits of account number

        self.table.setRowCount(len(users))

        for i, user in enumerate(users):
            # Make user be a list instead of a tuple
            user = list(user)
            user[9] = '*' * (len(user[9]) - 4) + user[9][-4:]
            for j, value in enumerate(user):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
                if j == 0:
                    self.table.item(i, j).setFlags(QtCore.Qt.ItemIsEnabled)

    def remove_user(self):
        selected_row = self.table.selectedIndexes()
        user_ids_to_remove = []
        for i in range(0, len(selected_row), SELECTED_ROW_CONSTANT):
            if i % SELECTED_ROW_CONSTANT == 0:
                user_id = self.table.item(selected_row[i].row(), 0).text()
                user_ids_to_remove.append(user_id)

        for user_id in user_ids_to_remove:
            self.controller.remove_user(user_id)

        self.populate_table()

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a1.type() == QtCore.QEvent.MouseMove:
            print("Mouse moved")
            # Restart timer
            self.timer.stop()
            self.timer.start(300000)
            print(self.timer.remainingTime())

        return super().eventFilter(a0, a1)
