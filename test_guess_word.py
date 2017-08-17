import pytest
from hangman.game import GuessWord
from hangman.exceptions import *


def test_guessed_word_interface():
    word = GuessWord('xyz')
    assert word.answer == 'xyz'
    assert word.masked == '***'


def test_guess_word_with_empty_word():
    """Words are empty."""
    with pytest.raises(InvalidWordException):
        GuessWord('')


def test_guess_word_with_invalid_character():
    """Character to guess has len() > 1."""
    word = GuessWord('aaa')
    with pytest.raises(InvalidGuessedLetterException):
        word.perform_attempt('xyz')


def test_guess_word_with_correct_character():
    word = GuessWord('Python')
    attempt = word.perform_attempt('y')

    assert attempt.is_hit() is True
    assert attempt.is_miss() is False

    assert word.masked == '*y****'


def test_guess_word_with_miss_character():
    word = GuessWord('Python')
    attempt = word.perform_attempt('z')

    assert attempt.is_miss() is True
    assert attempt.is_hit() is False

    assert word.masked == '******'


def test_guess_word_with_repeated_elements():
    word = GuessWord('rmotr')
    attempt = word.perform_attempt('r')

    assert attempt.is_hit() is True
    assert attempt.is_miss() is False

    assert word.masked == 'r***r'


def test_guess_word_with_all_equal_characters():
    word = GuessWord('aaa')
    attempt = word.perform_attempt('a')

    assert attempt.is_hit() is True
    assert attempt.is_miss() is False

    assert word.masked == 'aaa'


def test_guess_word_with_misses_and_guesses():
    word = GuessWord('Python')

    # Guess 'y' -- Hit!
    attempt = word.perform_attempt('y')
    assert attempt.is_hit() is True
    assert word.masked == '*y****'

    # Guess 'z' -- Miss!
    attempt = word.perform_attempt('z')
    assert attempt.is_miss() is True
    assert word.masked == '*y****'

    # Guess 'n' -- Hit!
    attempt = word.perform_attempt('n')
    assert attempt.is_hit() is True
    assert word.masked == '*y***n'

    # Guess 'o' -- Hit!
    attempt = word.perform_attempt('o')
    assert attempt.is_hit() is True
    assert word.masked == '*y**on'

    # Guess 'x' -- Miss!
    attempt = word.perform_attempt('x')
    assert attempt.is_miss() is True
    assert word.masked == '*y**on'

    # Guess 'a' -- Miss!
    attempt = word.perform_attempt('a')
    assert attempt.is_miss() is True
    assert word.masked == '*y**on'


def test_uncover_word_is_case_insensitive_same_case():
    word = GuessWord('Python')
    attempt = word.perform_attempt('P')

    assert attempt.is_hit() is True
    assert attempt.is_miss() is False

    assert word.masked == 'p*****'


def test_uncover_word_is_case_insensitive_different_case():
    word = GuessWord('Python')
    attempt = word.perform_attempt('p')

    assert attempt.is_hit() is True
    assert attempt.is_miss() is False

    assert word.masked == 'p*****'
