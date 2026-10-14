import random

print('ЧЕГО СКАЗАТЬ-ТО ХОТЕЛ, МИЛОК?!')
goodbyes = 0

while True:
    answer = input('> ')

    if answer == 'ПОКА!':
        goodbyes += 1
    else:
        goodbyes = 0

    if goodbyes == 3:
        print('ДО СВИДАНИЯ, МИЛЫЙ!')
        break


    if answer.upper() == answer and answer.lower() != answer:
        year = random.randint(1930, 1950)
        print('НЕТ, НИ РАЗУ С {0} ГОДА!'.format(year))
    else:
        print('АСЬ?! ГОВОРИ ГРОМЧЕ, ВНУЧЕК!')
