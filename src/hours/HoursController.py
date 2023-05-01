
from PyQt5 import QtWidgets
from src.RUPaid.Crypt import Hashing
from src.employee.EmployeeView import EmployeeView
from src.RUPaid.DatabaseConnection import DBConnection
from src.hours.HoursView import HoursView
from PyQt5.QtWidgets import QApplication
import sys
from src.RUPaid.DatabaseConnection import DBConnection
from PyQt5.QtCore import *

from datetime import datetime, date
from datetime import timedelta
import calendar

class HoursController:
    def __init__(self, user_id, employee_id):
        self.user_id = user_id
        self.employee_id = employee_id
        
        self.db_connection = DBConnection()
        self.populate_table()
        self.ui = HoursView(self)
        self.ui.show()

    def get_date_ranges(self):
        today = date.today()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start, end
    
    def get_all_hours(self, start, end):
        hours = self.db_connection.get_employees_hours(start, end, self.employee_id)
        hours = hours.fetchall()
        return hours
            
    def populate_table(self):
        start, end = self.get_date_ranges()
        start_day = start.day
        end_day = end.day
        monday = start_day
        tuesday = start_day + 1
        wednesday = start_day + 2
        thursday = start_day + 3
        friday = start_day + 4
        saturday = start_day + 5
        sunday = start_day + 6
        x = calendar.monthrange(datetime.now().year, 4)
        
        hours = self.get_all_hours(start, end)
        for row in hours:
            print(row)
            temp_start_day = row[1].day
            
            temp_start_time = row[1].time()
            temp_end_time = row[2].time()
            temp_hours_worked = row[3].time()
            start_string = f"Clock In Time: {temp_start_time}"
            end_string = f"Clock Out Time: {temp_end_time}"
            hours_string = f"Hours Worked: {temp_hours_worked}"
            if(temp_start_day == monday):
                # self.ui.hoursTable.setItem(1,0, QtWidgets.QTableWidgetItem(start_string))
                pass

app = QApplication(sys.argv)
t = HoursController(8, 50)

t.ui.show()
sys.exit(app.exec_())





