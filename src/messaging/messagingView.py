import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, \
    QAbstractItemView, QListWidgetItem
from PyQt5.QtGui import QFontDatabase


class MessagingView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.setMinimumSize(500,440)
        self.setMaximumSize(500, 440)
        self.controller = controller
        self.setWindowTitle("RUPaid - Messaging")
        self.timer = QtCore.QTimer() # TODO: Create the function for this
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
        self.title.setText("Messages")

        # Add the title to the title layout
        title_layout.addWidget(self.title, 0, 0, alignment=QtCore.Qt.AlignCenter)

        # Make the two buttons right next to each other
        self.messages = QtWidgets.QListWidget()
        self.messageSendTextEdit = QtWidgets.QTextEdit()
        self.messageSendTextEdit.setFixedSize(461,40)
        self.recipientSelection = QtWidgets.QComboBox()
        self.recipientSelection.activated.connect(lambda: self.controller.get_selected_conversation(self.recipientSelection.currentText()))
        self.sendButton = QtWidgets.QPushButton('Send')
        self.sendButton.clicked.connect(lambda: self.controller.send_message(self.messageSendTextEdit.toPlainText()))
        
        layout.addLayout(title_layout, stretch=1)
        layout.addWidget(self.recipientSelection)
        layout.addWidget(self.messages)
        layout.addWidget(self.messageSendTextEdit)
        layout.addWidget(self.sendButton)
        

        # Add a gray dividing line
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        divider.setStyleSheet("background-color: gray; height: 1px;")
        self.setLayout(layout)



    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a1.type() == QtCore.QEvent.MouseMove:
            print("Mouse moved")
            # Restart timer
            self.timer.stop()
            self.timer.start(300000)
            print(self.timer.remainingTime())

        return super().eventFilter(a0, a1)
# app = QApplication(sys.argv)
# t = MessagingView()
# t.show()
# sys.exit(app.exec_())