import os

from PyQt5.QtWidgets import QApplication

import sys

from src.RUPaid.Login import LoginPage


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        login_page = LoginPage()
        login_page.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)

