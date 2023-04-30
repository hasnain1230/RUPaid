from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QWidget, QMessageBox


from src.RUPaid.DatabaseConnection import DBConnection
from src.employee.ChangePasswordWindow import ChangePasswordWindow


class EmployeeView(QWidget):
    def __init__(self, controller):
        super(EmployeeView, self).__init__()
        self.change_password_dialog = None
        self.change_password_button = None
        self.edit_button = None
        self.grid_layout = None
        self.title = None
        self.clock_in_button = None
        self.dbConnection = DBConnection()
        self.controller = controller
        self.init_ui()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.controller.logout(timer=self.timer))
        self.timer.start(300000)
        self.installEventFilter(self)
        self.setWindowTitle("RUPaid - Employee")

    def init_ui(self):
        self.setFixedSize(1100, 440)

        layout = QtWidgets.QVBoxLayout()
        self.setWindowTitle("RUPaid - Employee")

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

        self.clock_in_button = QtWidgets.QPushButton("Clock In")
        self.clock_in_button.clicked.connect(self.clock_in)
        title_layout.addWidget(self.clock_in_button, 0, 1, alignment=QtCore.Qt.AlignRight)

        # Add Edit Button
        self.edit_button = QtWidgets.QPushButton("Edit Information")
        self.edit_button.clicked.connect(self.edit_information)
        title_layout.addWidget(self.edit_button, 0, 2, alignment=QtCore.Qt.AlignRight)

        # Add Change Password Button
        self.change_password_button = QtWidgets.QPushButton("Change Password")
        self.change_password_button.clicked.connect(self.change_password)
        title_layout.addWidget(self.change_password_button, 0, 3, alignment=QtCore.Qt.AlignRight)

        # Add logout button
        logout_button = QtWidgets.QPushButton("Logout")
        logout_button.clicked.connect(lambda: self.controller.logout(timer=self.timer))
        title_layout.addWidget(logout_button, 0, 4, alignment=QtCore.Qt.AlignRight)

        # Make the two buttons right next to each other
        title_layout.setColumnStretch(0, 1)

        layout.addLayout(title_layout, stretch=1)

        # Add a gray dividing line
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        divider.setStyleSheet("background-color: gray; height: 1px;")
        layout.addWidget(divider, alignment=QtCore.Qt.AlignTop, stretch=1)

        # Grid layout for the employee information
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setContentsMargins(20, 5, 20, 20)  # Add padding to the grid layout
        self.grid_layout.setSpacing(10)

        # Set a font for the grid labels
        grid_label_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont)
        grid_label_font.setPointSize(14)

        # Set size policy for labels and value labels to expand in both horizontal and vertical directions
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Add the employee information to the grid layout
        for row, (label_text, value) in enumerate([
            ("User ID:", str(self.controller.user_id)),
            ("First Name:", self.controller.first_name),
            ("Last Name:", self.controller.last_name),
            ("Age:", str(self.controller.age)),
            ("Occupation:", self.controller.occupation),
            ("Email:", self.controller.email),
            ("Bank Account Number:", self.controller.account_number),
            ("Bank Routing Number:", self.controller.routing_number),
        ]):
            label = QtWidgets.QLabel(label_text)
            label.setFont(grid_label_font)
            label.setSizePolicy(size_policy)
            self.grid_layout.addWidget(label, row, 0)

            value_label = QtWidgets.QLabel(value)
            value_label.setFont(grid_label_font)
            value_label.setSizePolicy(size_policy)
            self.grid_layout.addWidget(value_label, row, 1)

        layout.addLayout(self.grid_layout)

        # Set the layout
        self.setLayout(layout)

    def edit_information(self):
        for row in range(5, self.grid_layout.rowCount()):
            value_label = self.grid_layout.itemAtPosition(row, 1).widget()

            if not isinstance(value_label, QtWidgets.QLineEdit) and isinstance(value_label, QtWidgets.QLabel):
                value = value_label.text()
                value_edit = QtWidgets.QLineEdit()
                value_edit.setText(value)
                value_edit.returnPressed.connect(lambda: (self.controller.save_information(self.grid_layout), self.post_save()))
                self.grid_layout.replaceWidget(value_label, value_edit)
                value_label.deleteLater()

        self.edit_button.setText("Save Changes")
        self.edit_button.clicked.disconnect()
        self.edit_button.clicked.connect(lambda: (self.controller.save_information(self.grid_layout), self.post_save()))

    def post_save(self):
        self.edit_button.setText("Edit Information")
        self.edit_button.clicked.disconnect()

        for row in range(5, self.grid_layout.rowCount()):
            value_edit = self.grid_layout.itemAtPosition(row, 1).widget()

            if isinstance(value_edit, QtWidgets.QLineEdit):
                value = value_edit.text()

                if row == 6:  # If row is bank account number, replace all but last 4 digits with asterisks
                    value = "*" * (len(value) - 4) + value[-4:]

                grid_label_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont)
                grid_label_font.setPointSize(14)

                # Set size policy for labels and value labels to expand in both horizontal and vertical directions
                size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

                value_label = QtWidgets.QLabel(value)
                value_label.setFont(grid_label_font)
                value_label.setSizePolicy(size_policy)

                self.grid_layout.replaceWidget(value_edit, value_label)
                value_edit.deleteLater()

        self.edit_button.clicked.connect(self.edit_information)

    def clock_in(self):
        self.controller.clock_in()
        time_checked_in = self.controller.get_time_checked_in(
            user_id=self.grid_layout.itemAtPosition(0, 1).widget().text())

        # time_checked_in_label = time_checked_in + timedelta(minutes=7.5)
        # time_checked_in_label = time_checked_in_label - timedelta(minutes=time_checked_in_label.minute % 15, seconds=time_checked_in_label.second, microseconds=time_checked_in_label.microsecond)

        # As 24 hour time
        time_checked_in = time_checked_in.strftime("%H:%M")

        QMessageBox.information(self, "Clocked In", f"You have been clocked in at {time_checked_in}!")
        self.clock_in_button.setText("Clock Out")
        self.clock_in_button.clicked.disconnect()
        self.clock_in_button.clicked.connect(self.clock_out)

    def clock_out(self):
        self.controller.clock_out()
        time_checked_out = self.controller.get_time_checked_out(
            user_id=self.grid_layout.itemAtPosition(0, 1).widget().text())

        # As 24 hour time
        time_checked_out = time_checked_out.strftime("%H:%M")

        QMessageBox.information(self, "Clocked Out", f"You have been clocked out at {time_checked_out}!")
        self.clock_in_button.setText("Clock In")
        self.clock_in_button.clicked.disconnect()
        self.clock_in_button.clicked.connect(self.clock_in)

    def change_password(self):
        self.change_password_dialog = ChangePasswordWindow(self.controller)
        self.change_password_dialog.show()

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a1.type() == QtCore.QEvent.MouseMove:
            print("Mouse moved")
            # Restart timer
            self.timer.stop()
            self.timer.start(300000)
            print(self.timer.remainingTime())

        return super().eventFilter(a0, a1)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        print(f"Window resized to {self.width()}x{self.height()}")
