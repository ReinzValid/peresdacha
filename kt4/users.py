class User:
    count = 0

    def __init__(self, name, login, password, grade):
        if not isinstance(grade, int) or isinstance(grade, bool) or grade <= 0:
            raise ValueError('grade должен быть целым положительным числом.')
        self._name = name
        self.__login = login
        self.__password = password
        self.__grade = grade

        type(self).count += 1

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, value):
        message = 'Невозможно изменить логин!'
        print(message)
        return message

    @property
    def password(self):
        return '********'

    @password.setter
    def password(self, value):
        self.__password = value

    @property
    def grade(self):
        return 'Неизвестное свойство grade'

    @grade.setter
    def grade(self, value):
        message = 'Неизвестное свойство grade'
        print(message)
        return message

    def show_info(self):
        print('Name: {0}, Login: {1}'.format(self.name, self.login))

    def showInfo(self):

        self.show_info()

    def eq(self, other):
        return self.__eq__(other)

    def lt(self, other):
        return self.__lt__(other)

    def gt(self, other):
        return self.__gt__(other)

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.__grade == other.__grade

    def __lt__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.__grade < other.__grade

    def __gt__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.__grade > other.__grade


class SuperUser(User):
    count = 0

    def __init__(self, name, login, password, role, grade):
        super().__init__(name, login, password, grade)
        self._role = role

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    def show_info(self):
        print('Name: {0}, Login: {1}, Role: {2}'.format(self.name, self.login, self.role))
