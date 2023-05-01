from PyQt5 import QtWidgets

from src.RUPaid.Crypt import Hashing
from src.employee.EmployeeView import EmployeeView
from src.RUPaid.DatabaseConnection import DBConnection
from src.messaging.MessagingView import MessagingView

from PyQt5.QtWidgets import QApplication
import sys
from src.RUPaid.DatabaseConnection import DBConnection

from PyQt5.QtCore import *


class MessagingController:
    def __init__(self, user_id):
        self.user_id = user_id
        self.db_connection = DBConnection()
        self.ui = MessagingView(self)
        self.ui.show()
        self.populate_recipients_list()

    # gets all messages relating to user from db, and populates ui listWidget
    def populate_messages_list(self, recipient_id):
        messages_cursor = self.db_connection.get_employee_conversation(self.user_id, recipient_id)
        self.ui.messages.clear()
        for i in messages_cursor:
            # string formatting
            message = str(i[6]) + "    " + str(i[4])
            if len(message) > 40:
                message = self.wrap_message(message + '\n')
            messageWidgetItem = QtWidgets.QListWidgetItem(message)
            if i[0] == self.user_id:
                messageWidgetItem.setTextAlignment(Qt.AlignRight)
            else:
                messageWidgetItem.setTextAlignment(Qt.AlignLeft)
            self.ui.messages.addItem(messageWidgetItem)

    def wrap_message(self, message):
        wrappedMessage = ""
        for i, char in enumerate(message):
            if (i % 40 == 0):
                wrappedMessage += '\n'
            wrappedMessage += char
        return wrappedMessage

    # Populates the recipients drop down box
    def populate_recipients_list(self):
        cursor = self.db_connection.select_other_users_from_table(self.user_id)
        for employee in cursor:
            firstName = employee[5]
            lastName = employee[6]
            role = employee[7]
            formatted_entitity = f'{lastName},  {firstName} - {role}'
            self.ui.recipientSelection.addItem(formatted_entitity)

    def get_selected_conversation(self, txt):
        tokens1 = txt.split(',')
        if (len(tokens1) < 2):
            return
        lastName = tokens1[0]
        tokens2 = tokens1[1].split(' ')

        firstName = tokens2[2]
        print(firstName + '-' + lastName)
        cursor = self.db_connection.get_user_id_by_name(firstName, lastName)
        selected_user_id = cursor.fetchall()[0][0]
        self.populate_messages_list(selected_user_id)
        return selected_user_id

    def send_message(self, message):
        print(self.ui.recipientSelection.currentText())
        recipient_id = self.get_selected_conversation(self.ui.recipientSelection.currentText())
        if (self.db_connection.insert_message(self.user_id, recipient_id, len(message), message)):
            # messaging failed to insert
            self.populate_messages_list(recipient_id)
