import re


def parse_book(line):

    fields = re.split(r'\|', line.strip())
    if len(fields) != 5:
        raise ValueError('В записи книги должно быть пять полей.')
    return fields[:3] + [int(fields[3]), float(fields[4])]


def get_books(filename):

    with open(filename, encoding='utf-8-sig') as source:
        lines = source.read().splitlines()
    if not lines or lines[0].strip() != 'isbn|title|author|quantity|price':
        raise ValueError('Неверный заголовок каталога.')
    return list(map(parse_book, filter(lambda line: bool(line.strip()), lines[1:])))


def filtered_books(books, parameter):

    selected = filter(lambda book: parameter.lower() in book[1].lower(), books)
    return list(map(lambda book: [book[0], book[1] + ', ' + book[2],
                                  book[3], book[4]], selected))


def total_prices(books):

    return list(map(lambda book: (book[0], round(book[2] * book[3], 2)), books))
