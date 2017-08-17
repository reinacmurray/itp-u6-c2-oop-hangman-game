try:
    # Python 2
    _input = raw_input
except NameError:
    # Python 3
    _input = input

from hangman.game import HangmanGame
from hangman.exceptions import *


def build_list_of_words(words):
    if words:
        return [w.strip() for w in words.split(',')]


def main():
    print("=====================")
    print("###### Hangman ######")
    print("=====================")
    words = _input("Enter your list of words separated by comma. Leave empty for default: ")

    if words.strip():
        words = build_list_of_words(words)
    else:
        words = None

    game = HangmanGame(word_list=words)

    print("\n### Game Initialized. Let's play!!\n")

    try:
        while True:
            print('')

            line_message = "({}) Enter new guess ({} remaining attempts): ".format(
                game.word.masked, game.remaining_misses)

            users_guess = _input(line_message)
            if not users_guess.strip():
                print("\tEmpty is not valid. Please guess again.")
                continue

            try:
                attempt = game.guess(users_guess)
            except InvalidGuessedLetterException:
                print("\t Your guess is incorrect. Please guess again.")
                continue

            if attempt.is_hit():
                print("\tCongratulations! That's correct.")
            else:
                print("\t:( That's a miss!")
    except GameWonException:
        print("\t YES! You win! The word was: {}".format(game.word.answer))
    except GameLostException:
        print("\t :( OH NO! You Lose! The word was: {}".format(game.word.answer))


if __name__ == '__main__':
    main()
