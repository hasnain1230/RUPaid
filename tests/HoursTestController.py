from src.RUPaid.Crypt import Hashing
from src.messaging.messagingController import MessagingController
from src.RUPaid.DatabaseConnection import DBConnection
from PyQt5.QtWidgets import QApplication

import sys

class MessagingControllerTest():
    def __init__(self, connection: DBConnection) -> None:
        self.connection = connection
        self.test_employee = [
            'Testing',
            1,
            42,
            'hasnain1230',
            'lucidity',
            'Hasnain',
            'Ali',
            'employee',
            21,
            'Software Engineer',
            'hasnain1230@gmail.com',
            '******2864',
            '8974658465'
        ]
        self.controller = MessagingController(self.test_employee[2], self.connection, True)
        
    def run_tests(self):
        self.test_wrap_message
        self.test_get_selected_recipient
    
    def test_wrap_message(self):
        text_to_be_wrapped = "Wrap this text Wrap this text Wrap this text Wrap this text Wrap this text"
        function_wrapped = self.controller.wrap_text()
        manually_wrapped = ""
        for i, char in enumerate(text_to_be_wrapped):
            if(i %40 == 0):
                manually_wrapped += '\n'
            manually_wrapped += char
        assert text_to_be_wrapped == manually_wrapped
    
    def test_get_selected_recipient(self):
        txt = "Hasnain, Ali - Employee"
        res = None
        if(txt.find(',') == -1):
            self.populate_messages_list(0)
            res = 0
        tokens1 = txt.split(',')
        if(len(tokens1) < 2):
            res = None
        lastName = tokens1[0]
        tokens2 = tokens1[1].split(' ')

        firstName = tokens2[2]
        cursor = self.db_connection.get_user_id_by_name(firstName, lastName)
        selected_user_id = cursor.fetchall()[0][0]   
        assert res == 42
    
    def test_send_message():
        self.controller.send_message()

app = QApplication(sys.argv)
testRunner = MessagingControllerTest(DBConnection())
testRunner.run_tests()