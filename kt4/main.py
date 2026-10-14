from users import User, SuperUser


def main():
    user1 = User('Paul McCartney', 'paul', '1234', 3)
    user2 = User('George Harrison', 'george', '5678', 2)
    user3 = User('Richard Starkey', 'ringo', '8523', 3)
    admin = SuperUser('John Lennon', 'john', '0000', 'admin', 5)
    user1.show_info()
    admin.show_info()
    print('Всего обычных пользователей:', User.count)
    print('Всего супер-пользователей:', SuperUser.count)
    print(user1 < user2)
    print(admin > user3)
    print(user1 == user3)
    user3.name = 'Ringo Starr'
    user1.password = 'Pa$$w0rd'
    print(user3.name)
    print(user2.password)
    print(user2.login)
    user2.login = 'geo'
    print(user1.grade)
    admin.grade = 10
    admin.role = 'editor'
    admin.show_info()


if __name__ == '__main__':
    main()
