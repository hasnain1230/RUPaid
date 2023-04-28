from PyQt5.QtWidgets import QApplication

import sys

from src.RUPaid.Login import LoginPage


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())

