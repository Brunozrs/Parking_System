from Model.User import User

class Worker(User):
    def __init__(self,salary:float ,password: str = "", role: str = "worker",**kwargs):
        super().__init__(**kwargs)
        self._salary = salary
        self._password = password
        self._role = role

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, salary):
        self._salary = salary

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, password):
        self._password = password

    @property
    def role(self):
        return self._role
    @role.setter
    def role(self, role):
        self._role = role
