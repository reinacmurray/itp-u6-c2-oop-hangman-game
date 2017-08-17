# Hangman Game

For today's project, we'll be rewriting our previous Hangman Game using OOP. We'll explore **fundamental design** concepts.

There will be three main classes:

* `HangmanGame`: the main interface for the user, the "general" game that will be used.
* `GuessWord`: A word to guess. Is used by a `HangmanGame` to keep track of the word to guess.
* `GuessAttempt`: An attempt to guess a letter.

Each one of these classes have its own test file where you can see in more detail their interfaces.

Before exploring each class in detail, let us show you a general Hangman match with the new OOP interface:

```python
game = HangmanGame(['abc'], number_of_guesses=5)

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

game.guess('b')  # Raises GameWonException!

# After the exception:
assert game.is_finished() is True
assert game.is_won() is True
assert game.is_lost() is False

assert game.remaining_misses == 3
assert game.previous_guesses == ['a', 'x', 'c', 'z', 'b']
assert game.word.masked == 'abc'
```

## `HangmanGame` class

```bash
$ py.test test_hangman_game.py
```

This is the main Game class that will keep control of the overall "game status". It'll receive guess attempts (`game.guess`), will check for general business logic/rules (if the game is not already finished, if there are remaining attempts available in this match, if the character wasn't used before, etc) and if everything goes well it'll just rely on the GuessWord class to "perform an attempt" (`guess_word.perform_attempt`).

The `HangmanGame` class has one classmethod `select_random_word` that receives a list of words and selects one randomly.


A `HangmanGame` is constructed by **optionally** passing a list of words and the number of attempts: `HangmanGame(word_list=['Python', 'rmotr'], number_of_guesses=3)`. But these parameters are optional, if not provided:

* the `number_of_guesses` should be 5
* the `word_list` should be taken from the class variable `HangmanGame.WORD_LIST` that should be equals to `['rmotr', 'python', 'awesome']`

```python
print(HangmanGame.WORD_LIST)  # ['rmotr', 'python', 'awesome']
```

## `GuessWord` class

```bash
$ py.test test_guess_word.py
```

`GuessWord` keeps track of the word to guess and the current state of the "masked" word. It is constructed by passing a word to guess (`GuessWord('xyz')`) and it has a public `perform_attempt` method that takes one character and returns a `GuessAttempt` (more details below). Here's its simple interface:

```python
word = GuessWord('xyz')
assert word.answer == 'xyz'
assert word.masked == '***'

attempt = word.perform_attempt('x')  # Hit!
assert word.masked == 'x**'

attempt = word.perform_attempt('a')  # Miss!
assert word.masked == 'x**'

attempt = word.perform_attempt('abc')  # Invalid! Should raise InvalidGuessedLetterException.
assert word.masked == 'x**'
```

## `GuessAttempt` class

```bash
$ py.test test_guess_attempt.py
```

`GuessAttempt` objects are returned when an attempt is performed on a `GuessWord` object, they shouldn't be constructed manually outside of the `GuessWord.perform_attempt` method. A `GuessAttempt` has two methods `is_hit()` and `is_miss()` depending on the result of the attempt:

```python
word = GuessWord('xyz')

attempt = word.perform_attempt('x')  # Hit!
assert attempt.is_hit() is True
assert attempt.is_miss() is False

attempt = word.perform_attempt('a')  # Miss!
assert attempt.is_miss() is True
assert attempt.is_hit() is False
```


# Play the game!

As usual, you can use the `main.py` script to play the game once it's resolved.
