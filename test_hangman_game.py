import pytest
from hangman.game import HangmanGame, GuessWord
from hangman.exceptions import *


def test_select_random_word_with_one_word():
    list_of_words = ['rmotr']
    word_to_guess = HangmanGame.select_random_word(list_of_words)
    assert word_to_guess == 'rmotr'


def test_select_random_word_with_many_words():
    list_of_words = ['rmotr', 'python', 'intro']
    word_to_guess = HangmanGame.select_random_word(list_of_words)
    assert word_to_guess in list_of_words


def test_select_random_word_with_empty_list():
    with pytest.raises(InvalidListOfWordsException):
        HangmanGame.select_random_word([])


def test_start_new_game_initial_state_with_number_of_guesses():
    game = HangmanGame(['Python'], number_of_guesses=3)

    assert game.remaining_misses == 3
    assert isinstance(game.word, GuessWord)
    assert game.previous_guesses == []


def test_start_new_game_initial_state_with_default_attempts():
    game = HangmanGame(['Python'])

    assert game.remaining_misses == 5
    assert isinstance(game.word, GuessWord)
    assert game.previous_guesses == []


def test_start_new_game_initial_state_with_default_word_list():
    assert HangmanGame.WORD_LIST == ['rmotr', 'python', 'awesome']
    game = HangmanGame()

    assert game.remaining_misses == 5
    assert isinstance(game.word, GuessWord)
    assert game.previous_guesses == []

    assert game.word.answer in HangmanGame.WORD_LIST


def test_game_with_one_correct_guess():
    game = HangmanGame(['Python'])
    attempt = game.guess('y')

    assert attempt.is_hit() is True
    assert game.remaining_misses == 5
    assert game.previous_guesses == ['y']
    assert game.word.masked == '*y****'


def test_game_with_two_correct_guesses_same_move():
    game = HangmanGame(['rmotr'])
    attempt = game.guess('r')

    assert attempt.is_hit() is True
    assert game.remaining_misses == 5
    assert game.previous_guesses == ['r']
    assert game.word.masked == 'r***r'


def test_game_with_one_incorrect_guess():
    game = HangmanGame(['Python'])
    attempt = game.guess('x')  # Miss!

    assert attempt.is_miss() is True
    assert game.remaining_misses == 4
    assert game.previous_guesses == ['x']
    assert game.word.masked == '******'


def test_game_with_several_incorrect_guesses():
    game = HangmanGame(['Python'])

    attempt = game.guess('x')  # Miss!
    assert attempt.is_miss() is True
    assert game.remaining_misses == 4
    assert game.previous_guesses == ['x']
    assert game.word.masked == '******'

    attempt = game.guess('z')  # Miss!
    assert attempt.is_miss() is True
    assert game.remaining_misses == 3
    assert game.previous_guesses == ['x', 'z']
    assert game.word.masked == '******'


def test_game_with_several_correct_guesses():
    game = HangmanGame(['Python'])

    attempt = game.guess('y')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 5
    assert game.previous_guesses == ['y']
    assert game.word.masked == '*y****'

    attempt = game.guess('o')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 5
    assert game.previous_guesses == ['y', 'o']
    assert game.word.masked == '*y**o*'

    attempt = game.guess('t')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 5
    assert game.previous_guesses == ['y', 'o', 't']
    assert game.word.masked == '*yt*o*'


def test_game_with_several_correct_and_incorrect_guesses():
    game = HangmanGame(['Python'])

    attempt = game.guess('y')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 5
    assert game.previous_guesses == ['y']
    assert game.word.masked == '*y****'

    attempt = game.guess('x')  # Miss!
    assert attempt.is_miss() is True
    assert game.remaining_misses == 4
    assert game.previous_guesses == ['y', 'x']
    assert game.word.masked == '*y****'

    attempt = game.guess('o')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 4
    assert game.previous_guesses == ['y', 'x', 'o']
    assert game.word.masked == '*y**o*'

    attempt = game.guess('z')
    assert attempt.is_miss() is True
    assert game.remaining_misses == 3
    assert game.previous_guesses == ['y', 'x', 'o', 'z']
    assert game.word.masked == '*y**o*'


def test_guess_word_is_case_insensitve():
    game = HangmanGame(['Python'])

    attempt = game.guess('p')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 5
    assert game.previous_guesses == ['p']
    assert game.word.masked == 'p*****'

    attempt = game.guess('N')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 5
    assert game.previous_guesses == ['p', 'n']
    assert game.word.masked == 'p****n'


def test_game_wins_first_try():
    game = HangmanGame(['aaa'])

    with pytest.raises(GameWonException):
        game.guess('a')

    assert game.is_finished() is True
    assert game.is_won() is True
    assert game.is_lost() is False

    assert game.remaining_misses == 5
    assert game.previous_guesses == ['a']
    assert game.word.masked == 'aaa'


def test_game_loses_first_try():
    game = HangmanGame(['Python'], number_of_guesses=1)

    with pytest.raises(GameLostException):
        game.guess('x')  # Miss!

    assert game.is_finished() is True
    assert game.is_lost() is True
    assert game.is_won() is False

    assert game.remaining_misses == 0
    assert game.previous_guesses == ['x']
    assert game.word.masked == '******'


def test_game_wins_several_moves_repeated_words():
    game = HangmanGame(['aba'])

    attempt = game.guess('a')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 5
    assert game.previous_guesses == ['a']
    assert game.word.masked == 'a*a'

    with pytest.raises(GameWonException):
        game.guess('b')

    assert game.is_finished() is True
    assert game.is_won() is True
    assert game.is_lost() is False

    assert game.remaining_misses == 5
    assert game.previous_guesses == ['a', 'b']
    assert game.word.masked == 'aba'


def test_game_wins_several_moves():
    game = HangmanGame(['abc'])

    attempt = game.guess('a')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 5
    assert game.previous_guesses == ['a']
    assert game.word.masked == 'a**'

    attempt = game.guess('c')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 5
    assert game.previous_guesses == ['a', 'c']
    assert game.word.masked == 'a*c'

    with pytest.raises(GameWonException):
        game.guess('b')

    assert game.is_finished() is True
    assert game.is_won() is True
    assert game.is_lost() is False

    assert game.remaining_misses == 5
    assert game.previous_guesses == ['a', 'c', 'b']
    assert game.word.masked == 'abc'


def test_game_wins_several_moves_some_misses():
    game = HangmanGame(['abc'])

    attempt = game.guess('a')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 5
    assert game.previous_guesses == ['a']
    assert game.word.masked == 'a**'

    attempt = game.guess('x')  # Miss!
    assert attempt.is_miss() is True
    assert game.remaining_misses == 4
    assert game.previous_guesses == ['a', 'x']
    assert game.word.masked == 'a**'

    attempt = game.guess('c')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 4
    assert game.previous_guesses == ['a', 'x', 'c']
    assert game.word.masked == 'a*c'

    attempt = game.guess('z')  # Miss!
    assert attempt.is_miss() is True
    assert game.remaining_misses == 3
    assert game.previous_guesses == ['a', 'x', 'c', 'z']
    assert game.word.masked == 'a*c'

    with pytest.raises(GameWonException):
        game.guess('b')

    assert game.is_finished() is True
    assert game.is_won() is True
    assert game.is_lost() is False

    assert game.remaining_misses == 3
    assert game.previous_guesses == ['a', 'x', 'c', 'z', 'b']
    assert game.word.masked == 'abc'


def test_game_loses_several_guesses():
    game = HangmanGame(['Python'], number_of_guesses=3)

    attempt = game.guess('x')  # Miss!
    assert attempt.is_miss() is True
    assert game.remaining_misses == 2
    assert game.previous_guesses == ['x']
    assert game.word.masked == '******'

    attempt = game.guess('z')  # Miss!
    assert attempt.is_miss() is True
    assert game.remaining_misses == 1
    assert game.previous_guesses == ['x', 'z']
    assert game.word.masked == '******'

    with pytest.raises(GameLostException):
        game.guess('a')  # Miss!

    assert game.is_finished() is True
    assert game.is_lost() is True
    assert game.is_won() is False

    assert game.remaining_misses == 0
    assert game.previous_guesses == ['x', 'z', 'a']
    assert game.word.masked == '******'


def test_game_loses_with_some_correct_guesses():
    game = HangmanGame(['Python'], number_of_guesses=3)

    attempt = game.guess('y')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 3
    assert game.previous_guesses == ['y']
    assert game.word.masked == '*y****'

    attempt = game.guess('x')  # Miss!
    assert attempt.is_miss() is True
    assert game.remaining_misses == 2
    assert game.previous_guesses == ['y', 'x']
    assert game.word.masked == '*y****'

    attempt = game.guess('z')  # Miss!
    assert attempt.is_miss() is True
    assert game.remaining_misses == 1
    assert game.previous_guesses == ['y', 'x', 'z']
    assert game.word.masked == '*y****'

    attempt = game.guess('t')
    assert attempt.is_hit() is True
    assert game.remaining_misses == 1
    assert game.previous_guesses == ['y', 'x', 'z', 't']
    assert game.word.masked == '*yt***'

    with pytest.raises(GameLostException):
        game.guess('a')  # Miss!

    assert game.is_finished() is True
    assert game.is_lost() is True
    assert game.is_won() is False

    assert game.remaining_misses == 0
    assert game.previous_guesses == ['y', 'x', 'z', 't', 'a']
    assert game.word.masked == '*yt***'


def test_game_already_won_raises_game_finished():
    game = HangmanGame(['aaa'])

    with pytest.raises(GameWonException):
        game.guess('a')

    assert game.is_finished() is True
    assert game.is_won() is True
    assert game.is_lost() is False

    with pytest.raises(GameFinishedException):
        game.guess('x')


def test_game_already_lost_raises_game_finished():
    game = HangmanGame(['Python'], number_of_guesses=1)

    with pytest.raises(GameLostException):
        game.guess('x')  # Miss!

    assert game.is_finished() is True
    assert game.is_lost() is True
    assert game.is_won() is False

    with pytest.raises(GameFinishedException):
        game.guess('n')
