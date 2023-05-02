from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QTabWidget, QWidget


class UserHistory(QMainWindow):
    def __init__(self, user_id, controller):
        super().__init__()

        self.controller = controller

        self.setWindowTitle("RUPaid - User History")
        self.setMinimumSize(650, 600)
        self.user_id = user_id

        # Set up the tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Add payment history tab
        self.payment_history_tab = QWidget()
        self.payment_history_layout = QVBoxLayout(self.payment_history_tab)
        self.payment_history_table = QTableWidget()
        self.payment_history_layout.addWidget(self.payment_history_table)
        self.tab_widget.addTab(self.payment_history_tab, "User Payment History")

        # Add clock-in history tab
        self.clock_in_history_tab = QWidget()
        self.clock_in_history_layout = QVBoxLayout(self.clock_in_history_tab)
        self.clock_in_history_table = QTableWidget()
        self.clock_in_history_layout.addWidget(self.clock_in_history_table)
        self.tab_widget.addTab(self.clock_in_history_tab, "Clock-in History")

        # Set up table headers and populate tables
        self.setup_payment_history_table()
        self.setup_clock_in_history_table()

    def setup_payment_history_table(self):
        headers = ["User ID", "Payment Date", "Payment Amount", "Time Paid"]
        self.payment_history_table.setColumnCount(len(headers))
        self.payment_history_table.setHorizontalHeaderLabels(headers)
        self.payment_history_table.setAlternatingRowColors(True)
        self.payment_history_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Replace this with your data
        payment_data = self.controller.get_user_payment_history(self.user_id)

        self.payment_history_table.setRowCount(len(payment_data))
        for row, data in enumerate(payment_data):
            for column, item in enumerate(data):
                self.payment_history_table.setItem(row, column, QTableWidgetItem(str(item)))

    def setup_clock_in_history_table(self):
        headers = ["ID", "User_ID", "Clock In Time", "Clock Out Time", "Time Worked", "Paid"]
        self.clock_in_history_table.setColumnCount(len(headers))
        self.clock_in_history_table.setHorizontalHeaderLabels(headers)
        self.clock_in_history_table.setAlternatingRowColors(True)
        self.clock_in_history_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Replace this with your data
        clock_in_data = self.controller.get_user_clock_in_history(self.user_id)

        self.clock_in_history_table.setRowCount(len(clock_in_data))
        for row, data in enumerate(clock_in_data):
            for column, item in enumerate(data):
                self.clock_in_history_table.setItem(row, column, QTableWidgetItem(str(item)))