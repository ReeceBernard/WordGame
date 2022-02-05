from english_words import english_words_lower_set
from errors import InvalidWordLengthError
import numpy as np
import json
import os


class Wordgame:
    def __init__(self, num_letters) -> None:
        self.get_previous_used_words()
        self.game_over = False
        self.word = None
        self.num_guesses = 0
        self.winner = False
        self.guessed_words = set()
        self.num_letters = num_letters
        self.game_string = ""

    def get_previous_used_words(self):
        if os.stat("wordgame/words_used.json").st_size == 0:
            self.words_used = set()
            return
        with open("wordgame/words_used.json", "r") as read_file:
            data = json.load(read_file)
        self.words_used = set(data)

    def add_word_to_used_list(self):
        self.words_used.add(self.word)
        data = list(self.words_used)
        with open("wordgame/words_used.json", "w") as write_file:
            json.dump(data, write_file)

    def pick_word(self):
        if self.num_letters == 5:
            possible_words = [
                key
                for key in english_words_lower_set
                if len(key) == 5 and key not in self.words_used
            ]
        elif self.num_letters == 6:
            possible_words = [
                key
                for key in english_words_lower_set
                if len(key) == 6 and key not in self.words_used
            ]
        elif self.num_letters == 7:
            possible_words = [
                key
                for key in english_words_lower_set
                if len(key) == 7 and key not in self.words_used
            ]
        else:
            raise InvalidWordLengthError
        if len(possible_words) == 0:
            self.words_used = set()
            self.pick_word()
        self.word = np.random.choice(possible_words).upper()
        self.add_word_to_used_list()

    def check_valid_input(self, user_input):
        if len(user_input) != self.num_letters:
            print(f"Error {user_input} is not a {self.num_letters} letter word.")
            return False
        if user_input.lower() not in english_words_lower_set:
            print("Not a valid english word.")
            return False
        input = user_input.upper()
        if input in self.guessed_words:
            print(f"You have already guessed {user_input}")
            return False
        return True

    def get_user_input(self):
        valid = False
        while not valid:
            text = input(f"Please guess a {self.num_letters} letter word: ")
            valid = self.check_valid_input(text)
        self.guessed_words.add(text.upper())
        return text.upper()

    def update_game(self, user_input):
        self.num_guesses += 1
        if user_input == self.word:
            # turn letters green
            self.winner = True
            self.game_over = True
            return
        letters = list(user_input)
        goal_letters = list(self.word)
        for i, letter in enumerate(letters):
            if letter == goal_letters[i]:
                self.game_string += f"{letter}g,"
            elif letter in goal_letters:
                self.game_string += f"{letter}y,"
            else:
                self.game_string += f"{letter}b,"
        self.game_string = self.game_string[:-1]
        print(self.game_string)
        self.game_string += "\n"
        if user_input == self.word:
            self.winner = True
            self.game_over = True
        if self.num_guesses > 6:
            self.game_over = True

    def display_game_over_screen(self):
        if self.winner:
            print(f"You won in {self.num_guesses} guesses!")
        else:
            print(f"The word was {self.word} you dumbass.")

    def play_game(self):
        self.pick_word()
        while not self.game_over:
            user_input = self.get_user_input()
            self.update_game(user_input)

        self.display_game_over_screen()


if __name__ == "__main__":
    wordle = Wordgame(5)
    wordle.play_game()
