from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase, QRegExpValidator

from src.employer.AddUserWindow import AddUser
from src.employer.ResetPassword import ResetPassword
from src.employer.EditWindow import EditDialog
from src.employer.UserHistory import UserHistory
from src.messaging.MessagingController import MessagingController
from src.messaging.MessagingView import MessagingView

SELECTED_ROW_CONSTANT = 10


class EmployerView(QWidget):
    def __init__(self, controller):
        super().__init__(parent=None)
        self.view_hours = None
        self.message_view = None
        self.messaging_controller = None
        self.hours_controller = None
        self.hours_view = None
        self.edit_dialog = None
        self.reset_password = None
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
        self.title = QtWidgets.QLabel()
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
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table.doubleClicked.connect(lambda: self.edit_user())
        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.itemDoubleClicked.connect(lambda: self.edit_user())
        self.table.itemClicked.connect(lambda: self.reset_timer())

        # Install event listener when field is edited
        self.table.itemSelectionChanged.connect(self.prepare_buttons)
        # Allow columns to be resized
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.table.setStyleSheet("QTableWidget::item { padding: 10px; }")
        self.populate_table()
        layout.addWidget(self.table, stretch=11)

        button_layout = QtWidgets.QHBoxLayout()

        button_layout.addStretch(0)

        # Message User
        self.message_user_button = QtWidgets.QPushButton("View Messages")
        self.message_user_button.clicked.connect(self.message_button)
        button_layout.addWidget(self.message_user_button, alignment=QtCore.Qt.AlignLeft)

        button_layout.addStretch(1)

        # Refresh Button
        refresh_button = QtWidgets.QPushButton("Refresh")
        refresh_button.clicked.connect(lambda: self.populate_table())
        button_layout.addWidget(refresh_button, alignment=QtCore.Qt.AlignRight)

        # Change Password
        self.change_password_button = QtWidgets.QPushButton("Reset Password")
        self.change_password_button.setDisabled(True)
        self.change_password_button.clicked.connect(self.change_password)
        button_layout.addWidget(self.change_password_button, alignment=QtCore.Qt.AlignRight)

        # View User Hours
        self.view_hours_button = QtWidgets.QPushButton("View User Hours / Payment History")
        self.view_hours_button.setDisabled(True)
        self.view_hours_button.clicked.connect(self.view_hours_action)
        button_layout.addWidget(self.view_hours_button, alignment=QtCore.Qt.AlignRight)

        # Pay User
        self.pay_user_button = QtWidgets.QPushButton("Pay User")
        self.pay_user_button.setDisabled(True)
        self.pay_user_button.clicked.connect(self.pay_user_action)
        button_layout.addWidget(self.pay_user_button, alignment=QtCore.Qt.AlignRight)

        # Add user button
        add_user_button = QtWidgets.QPushButton("Add User")
        # Add user function and populate table again
        add_user_button.clicked.connect(lambda: self.add_user())
        button_layout.addWidget(add_user_button, alignment=QtCore.Qt.AlignRight)

        # Edit User
        self.edit_user_button = QtWidgets.QPushButton("Edit User")
        self.edit_user_button.setDisabled(True)
        self.edit_user_button.clicked.connect(lambda: self.edit_user())
        button_layout.addWidget(self.edit_user_button, alignment=QtCore.Qt.AlignRight)

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

    def change_password(self):
        # Get the user id of the selected user
        user_id = self.table.item(self.table.currentRow(), 0).text()
        self.reset_password = ResetPassword(user_id, employer_controller=self.controller)
        self.reset_password.show()

    def view_hours_action(self):
        # Get the user id of the selected user
        user_id = self.table.item(self.table.currentRow(), 0).text()
        self.view_hours = UserHistory(user_id, self.controller)
        self.view_hours.show()

    def message_button(self):
        # Get selected user_id
        self.messaging_controller = MessagingController(self.controller.user_id, self.controller.company_name_id)
        self.message_view = MessagingView(self.messaging_controller)

    def prepare_buttons(self):
        selected_row = self.table.selectedIndexes()

        if len(selected_row) == SELECTED_ROW_CONSTANT:
            self.change_password_button.setDisabled(False)
            self.edit_user_button.setDisabled(False)
            self.pay_user_button.setDisabled(False)
            self.view_hours_button.setDisabled(False)
        else:
            self.change_password_button.setDisabled(True)
            self.edit_user_button.setDisabled(True)
            self.pay_user_button.setDisabled(True)
            self.view_hours_button.setDisabled(True)

        if len(selected_row) != 0 and len(selected_row) % SELECTED_ROW_CONSTANT == 0:
            self.remove_user_button.setDisabled(False)
        else:
            self.remove_user_button.setDisabled(True)

    def edit_user(self):
        self.edit_dialog = EditDialog(table=self.table, controller=self.controller)
        self.edit_dialog.show()

    def populate_table(self):
        users = self.controller.get_all_users()

        self.table.setRowCount(len(users))

        for i, user in enumerate(users):
            for j, value in enumerate(user):
                if j == 9:
                    value = '*' * (len(value) - 4) + value[-4:]
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
                if j == 0:
                    self.table.item(i, j).setFlags(QtCore.Qt.ItemIsEnabled)

    def remove_user(self):
        selected_row = self.table.selectedIndexes()
        user_ids_to_remove = []
        for i in range(0, len(selected_row), SELECTED_ROW_CONSTANT):
            if i % SELECTED_ROW_CONSTANT == 0:
                user_id = self.table.item(selected_row[i].row(), 0).text()

                if user_id == self.controller.user_id:
                    QtWidgets.QMessageBox.warning(self, "Error", "You cannot remove yourself")
                    continue

                user_ids_to_remove.append(user_id)

        for user_id in user_ids_to_remove:
            self.controller.remove_user(user_id)

        self.populate_table()

    def pay_user_action(self):
        # Get selected user id
        user_id = self.table.item(self.table.currentRow(), 0).text()
        # Get user first and last name
        first_name = self.table.item(self.table.currentRow(), 2).text()
        last_name = self.table.item(self.table.currentRow(), 3).text()
        total_comp = self.controller.pay_user(user_id)

        if total_comp is None:
            return
        else:
            total_comp = round(total_comp, 2)

        QtWidgets.QMessageBox.information(self, "Success", f"Paid {first_name} {last_name} ${total_comp:.2f}")

    def reset_timer(self):
        self.timer.stop()
        self.timer.start(300000)
        print("Time Reset")

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a1.type() == QtCore.QEvent.MouseMove:
            print("Mouse moved")
            # Restart timer
            self.timer.stop()
            self.timer.start(300000)
            print(self.timer.remainingTime())

        return super().eventFilter(a0, a1)
