import mysql.connector


class DBConnection:
    def __init__(self):
        self.db = mysql.connector.connect(
            host = 'lucidityarch.com',
            user = 'allimg',
            passwd = 'allimg',
            database = 'RUPaid'
        )
        self.cursor = self.db.cursor()
    
    def executeQuery(self, query):
        return self.cursor.execute(query)
        
    def selectFromTable(self, table = 'users2'):
        self.cursor.execute(f'SELECT * FROM {table}')
        return self.cursor
    
    def selectNamesFromTable(self, table = 'users2'):
        self.cursor.execute(f'SELECT firstName, lastName FROM {table}')
        return self.cursor
    
    def getEmployeeByName(self, first, last, table ='users2'):
        self.cursor.execute(f"SELECT * from {table} WHERE firstName = '{first}' and lastName = '{last}'")
        return self.cursor
    
    def insertIntoTest_Table(self,  name, age):
        self.cursor.execute(f"INSERT INTO test_table (name, age) VALUES ('{name}', '{age}')")
        self.db.commit()
    