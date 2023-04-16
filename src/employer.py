class Employer:
    def __init__(self, firstName, lastName, email, pwd):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.pwd = pwd
    
    def getName(self):
        return f'{self.lastName}, {self.firstName}'
    
    def getEmail(self):
        return self.email
    
    def setPassword(self, pwd):
        self.pwd = pwd
    
    def setEmail(self, email):
        self.email = email