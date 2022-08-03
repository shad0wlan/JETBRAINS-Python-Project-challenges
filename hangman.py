# Write your code here
from random import choice


class WordGuess:
    used_values = set()
    
    def __init__(self, *words):
        self._wordlist = words
        self.word = choice(*self._wordlist)
        self.unique_words = set(self.word)
        self.empty_indexes = ["-" for _ in range(len(self.word))]
        self.max_attempts = 8
        self._play_state = True
        self.wins = 0
        self.loses = 0
        self.menu = {"play", "results", "exit"}
        self.game_state = True

    @property
    def state(self):
        return self._play_state

    def input_check(self, character):
        if len(character) != 1:
            print("Please, input a single letter.")
            return False
        if not character.isalpha() or character.isupper():
            print("Please, enter a lowercase letter from the English alphabet.")
            return False
        if character in self.unique_words:
            for i in range(len(self.word)):
                if self.word[i] == character:
                    self.empty_indexes[i] = character
                    self.unique_words.discard(character)
            return True

        elif character in self.empty_indexes or character in self.used_values:
            print(f"You've already guessed this letter.")
            return True

        else:
            self.max_attempts -= 1
            self.used_values.add(character)
            print(f"That letter doesn't appear in the word.")
            return True



    def results(self):
        return f'You won: {self.wins} times.\nYou lost: {self.loses} times.'

    def check_state(self):
        if len(self.unique_words) == 0:
            print(f"You guessed the word {self.word}!\nYou survived!")
            self.wins += 1
            self._play_state = False
        if self.max_attempts == 0:
            self.loses += 1
            self._play_state = False
            print("\nYou lost!")
            return False
        return True

    def game_start(self, player_choice):
        if player_choice == "results":
            print(self.results())
            return True
        elif player_choice == "play":
            self.play()
            return True
        elif player_choice == "exit":
            self.game_state = False
            return True
        else:
            print("Please make a choice that is included in the menu")
            return False

    def play(self):
        if self._play_state:
            pass
        else:
            self.reset_game()
            self._play_state = True
        while self._play_state:
            self.check_state()
            if self._play_state:
                print(self.__str__())
                player_char = input("Input a letter: ")
                self.input_check(player_char)
                if not self._play_state:
                    return False

    def reset_game(self):
        self.word = choice(*self._wordlist)
        self.unique_words = set(self.word)
        self.empty_indexes = ["-" for _ in range(len(self.word))]
        self.max_attempts = 8
        self.used_values = set()

    def __str__(self):
        return "\n" + "".join(self.empty_indexes)


game = WordGuess(["python", "java", "swift", "javascript"])
print("H A N G M A N")
while game.game_state:
    menu = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit: ')
    game.game_start(menu)


       