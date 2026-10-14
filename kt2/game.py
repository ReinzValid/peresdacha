import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORD_FILE = os.path.join(BASE_DIR, 'words.txt')
HIDDEN = '■'
MAX_LIVES = 6


def load_words(filename=WORD_FILE):

    words = []
    known = set()
    with open(filename, encoding='utf-8') as source:
        for number, line in enumerate(source, 1):
            if not line.strip():
                continue
            parts = line.strip().split('|', 1)
            if len(parts) != 2 or not parts[0].isalpha() or not parts[1].strip():
                raise ValueError('Неверная запись слова в строке {0}'.format(number))
            word = parts[0].lower()
            if word not in known:
                words.append((word, parts[1].strip()))
                known.add(word)
    if not words:
        raise ValueError('В файле нет слов для игры.')
    return words


def has_words(words):
    return bool(words)


def choose_word(words):

    pair = random.choice(words)
    words.remove(pair)
    return pair


def create_table(word):
    return [HIDDEN for letter in word]


def get_lives():
    return MAX_LIVES


def create_answers():
    return set()


def is_alive(lives):
    return lives > 0


def is_hidden(table):
    return HIDDEN in table


def prompt_answer():
    return input('Введите букву или всё слово: ').strip().lower()


def is_valid(answer):
    return bool(answer) and answer.isalpha()


def is_repeated(answer, answers):
    return answer in answers


def remember_answer(answer, answers):
    answers.add(answer)


def is_word_correct(word, answer):
    return word == answer


def is_letter_correct(word, answer):
    return len(answer) == 1 and answer in word


def reveal_word(word):
    return list(word)


def reveal_letter(word, table, letter):

    result = table.copy()
    for index, current in enumerate(word):
        if current == letter:
            result[index] = letter
    return result


def lose_life(lives):
    return lives - 1


def show_gallows(lives):
    filename = os.path.join(BASE_DIR, 'gallows', '{0}.txt'.format(MAX_LIVES - lives))
    with open(filename, encoding='utf-8') as drawing:
        print(drawing.read())


def show_description(description):
    print('\nЗагадка:', description)


def show_table(table):
    print(' '.join(table))


def show_lives(lives):
    print('Осталось жизней:', lives)


def show_invalid_answer():
    print('Введите букву или слово без цифр и знаков.')


def show_repeated_answer():
    print('Такой ответ уже был. Попробуйте другой.')


def show_result(word, table):
    show_table(table)
    if is_hidden(table):
        print('Вы проиграли. Было загадано слово:', word)
    else:
        print('Вы победили! Слово:', word)


def wants_another_round():
    return input('Сыграть ещё? (да/нет): ').strip().lower() == 'да'


def show_goodbye():
    print('Игра завершена. Спасибо за игру!')
