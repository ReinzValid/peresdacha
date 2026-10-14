import game

words = game.load_words()
while game.has_words(words):
    word, description = game.choose_word(words)
    table = game.create_table(word)
    lives = game.get_lives()
    answers = game.create_answers()
    game.show_description(description)
    game.show_gallows(lives)

    while game.is_alive(lives) and game.is_hidden(table):
        game.show_table(table)
        game.show_lives(lives)
        answer = game.prompt_answer()
        if not game.is_valid(answer):
            game.show_invalid_answer()
            continue
        if game.is_repeated(answer, answers):
            game.show_repeated_answer()
            continue
        game.remember_answer(answer, answers)
        if game.is_word_correct(word, answer):
            table = game.reveal_word(word)
        elif game.is_letter_correct(word, answer):
            table = game.reveal_letter(word, table, answer)
        else:
            lives = game.lose_life(lives)
            game.show_gallows(lives)

    game.show_result(word, table)
    if game.has_words(words) and not game.wants_another_round():
        break
game.show_goodbye()
