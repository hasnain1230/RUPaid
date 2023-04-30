from src.RUPaid.DatabaseConnection import DBConnection
from src.employer.EmployerView import EmployerView


class EmployerController:
    def __init__(self, employer_data, database_connection: DBConnection):
        self.employee_data = employer_data
        self.company_name = employer_data[0]
        self.company_name_id = employer_data[1]
        self.user_id = employer_data[2]
        self.username = employer_data[3]
        self.password_hash = employer_data[4]
        self.first_name = employer_data[5]
        self.last_name = employer_data[6]
        self.role = employer_data[7]
        self.age = employer_data[8]
        self.occupation = employer_data[9]
        self.email = employer_data[10]
        self.account_number = "*" * (len(employer_data[11]) - 4) + employer_data[11][-4:]
        self.routing_number = employer_data[12]
        self.db_connection = database_connection
        self.login_page = None

        self.ui = EmployerView(self)
        self.ui.show()
