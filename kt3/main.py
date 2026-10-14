import os
from books import get_books, filtered_books, total_prices


def main():
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'books.csv')
    books = get_books(filename)
    print('Все книги:', books)
    selected = filtered_books(books, 'python')
    print('Книги про Python:', selected)
    print('Стоимость:', total_prices(selected))


if __name__ == '__main__':
    main()
