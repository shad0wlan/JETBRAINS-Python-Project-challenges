# write your code here
import numpy as np
from random import choice
from copy import deepcopy
class Board:
    def __init__(self, dimension):
        self.dimension = dimension
        self.grid = [[f" " for _ in range(dimension)] for _ in range(1, dimension + 1)]
        self.grid_reset = deepcopy(self.grid)
        self.empty_boxes = dimension * dimension
        self.length = (dimension * 2) + 3
        self.state = True
        self.valid_values = [i for i in range(dimension)]
        self.max_value = max(self.valid_values) + 1
        self.player = "X"
        self.added_initial_start = False
        self.game_modes = ["easy", "user", "medium", "hard"]
        self.difficulty = None
        self.computer_move = None
        self.round = 0
        self.winner = None

    # Cosmetic function if we want to pre-register played cells
    def initial_cells(self):
        if self.added_initial_start:
            cells = input("Enter the cells: ")
            cells_arr = [i if i != "_" else " " for i in cells]
            if cells_arr.count("X") > cells_arr.count("O"):
                self.player_1 = "O"
                self.player_2 = "X"
            else:
                self.player_1 = "X"
                self.player_2 = "O"
            self.empty_boxes -= cells_arr.count("X") + cells_arr.count("O")
            x = np.array(cells_arr).reshape(self.dimension, self.dimension)
            self.grid = list(x)
            print(self.valid_values)
            print(self.__str__())
        print(self.__str__())

    def check_grid_values(self,mark_to_check=None):
        grid = self.grid
        winning_lines = {}
        computer_lines = {}

        for i in range(len(grid)):
            winning_lines[f'Row: {i + 1}'] = "".join(grid[i])
            computer_lines[(f'Row', i)] = "".join(grid[i])
            winning_lines[f'Column: {i + 1}'] = "".join([grid[j][i] for j in range(len(grid))])
            computer_lines[(f'Column', i)] = "".join([grid[j][i] for j in range(len(grid))])
            winning_lines[f'Diagonal: 1'] = "".join([grid[i][i] for i in range(len(grid))])
            winning_lines[f'Diagonal: 2'] = "".join([grid[i][(len(grid) - 1) - i] for i in range(len(grid))])
            computer_lines[(f'Diagonal 1', i)] = "".join([grid[i][i] for i in range(len(grid))])
            computer_lines[(f'Diagonal 2', i)] = "".join([grid[i][(len(grid) - 1) - i] for i in range(len(grid))])
        if mark_to_check is not None and self.round >= 1:
            for i, j in computer_lines.items():
                row = i[1]
                enemy = j.count(mark_to_check)
                move = j.count(self.player)
                empty = j.count(" ")
                if (move == 2 and empty) or (enemy == 2 and empty):
                    empty_cell = j.index(" ")
                    if i[0] == "Column":
                        self.computer_move = (empty_cell, row)
                        break
                    elif i[0] == "Row":
                        self.computer_move = (row, empty_cell)
                        break
                    elif i[0] == "Diagonal 1":
                        self.computer_move = (empty_cell, empty_cell)
                        break
                    elif i[0] == "Diagonal 2":
                        self.computer_move = (empty_cell, -empty_cell - 1)
                        break
                else:
                    continue
        return winning_lines.values()

    def check_valid_move(self, move, player):
        try:
            row, column = int(move[0]) - 1, int(move[1]) - 1
            if row not in self.valid_values or column not in self.valid_values:
                print(f"Coordinates should be from 1 to {self.max_value}!")
                return False
            if self.grid[row][column] in {"X", "O"}:
                print("This cell is occupied! Choose another one!")
                return False
            else:
                self.grid[row][column] = player.upper()
                self.empty_boxes -= 1
                print(self.__str__())
                return True
        except (ValueError, IndexError):
            print("You should enter numbers!")
            return False

    def get_possible_moves(self, board):
        moves = [(i, j) for i in range(self.dimension) for j in range(self.dimension) if board[i][j] == " "]
        return moves

    def check_winner(self, change_state=True) -> bool:
        grid_values = self.check_grid_values()
        if "X" * self.dimension in grid_values:
            self.winner = "X"
        elif "O" * self.dimension in grid_values:
            self.winner = "O"
        elif self.empty_boxes < 1:
            self.winner = "Draw"
        if self.winner is not None:
            if change_state:
                self.state = False
                if self.winner in {"X", "O"}:
                    print(f"{self.winner} wins")
                else:
                    print(self.winner)
            return True

        return False

    def computer_mode(self, mark, difficulty) -> bool:
        mark_to_check = "X" if mark == "O" else "O"
        available_moves = self.get_possible_moves(self.grid)
        if difficulty == "easy":
            print(f'Making move level "{difficulty}"')
            row, column = choice(available_moves)
            self.grid[row][column] = mark
        if difficulty == "medium":
            self.check_grid_values(mark_to_check)
            if self.round <= 1 or self.computer_move is None:
                row, column = choice(available_moves)
                self.grid[row][column] = mark
            if self.computer_move is not None:
                row, column = self.computer_move
                self.grid[row][column] = mark
                self.computer_move = None
        if difficulty == "hard":
            best_score = -800
            best_move = None
            for move in available_moves:
                row, column = move
                self.grid[row][column] = mark
                self.empty_boxes -= 1
                score = self.minimax(False, self.grid)
                self.empty_boxes += 1
                self.grid[row][column] = " "
                self.winner = None
                if score > best_score:
                    best_score = score
                    best_move = move
            row, column = best_move
            self.grid[row][column] = mark

        self.empty_boxes -= 1
        print(self.__str__())
        self.check_winner()
        return True

    def minimax(self, is_maximizer_turn, board):
        state = self.check_winner(False)
        if state:
            if self.winner == "Draw":
                return 0
            else:
                return 1 if self.winner == self.player else -1
        player = "X" if not is_maximizer_turn else "O"
        scores = []
        for move in self.get_possible_moves(board):
            row, column = move
            board[row][column] = player
            self.empty_boxes -= 1
            scores.append(self.minimax(not is_maximizer_turn, board))
            self.empty_boxes += 1
            board[row][column] = " "
        return max(scores) if is_maximizer_turn else min(scores)

    def start(self, player_1, player_2):
        if player_1 not in self.game_modes or player_2 not in self.game_modes:
            return False
        else:
            return True, player_1, player_2

    def reset_board(self):
        self.grid = deepcopy(self.grid_reset)

    def user_mode(self, player, mode="user") -> bool:
        if mode == "user":
            while True:
                player_move = input("Enter the coordinates: ").strip().split()
                if not self.check_valid_move(player_move, player):
                    continue
                self.round += 1
                self.check_winner()
                self.player = "O" if player == "X" else "X"
                return True
        else:
            if mode in {"easy", "medium", "hard"}:
                self.difficulty = mode
                self.computer_mode(self.player, self.difficulty)
                self.round += 1
                self.player = "O" if player == "X" else "X"
                return True

    def game(self):
        while True:
            input_command = input("Input command: ").split()
            if len(input_command) == 3:
                if input_command[0] == "start":
                    valid, player_1, player_2 = self.start(input_command[1], input_command[2])
                    if valid:
                        print(self.__str__())
                        while self.state:
                            self.user_mode(self.player, player_1)
                            if not self.state:
                                break
                            self.user_mode(self.player, player_2)
                        continue
                    else:
                        print("Bad parameters!")
                        continue
            if "".join(input_command) == "exit":
                break
            if "".join(input_command) == "reset":
                print("Re-register players")
                self.reset_board()
            else:
                print("Bad parameters!")

    def __str__(self):
        grid_visualization = ["-" * self.length]
        for i in self.grid:
            grid_visualization.append(" ".join(["|", *i, "|"]))
        grid_visualization.append("-" * self.length)
        return "\n".join(grid_visualization)


def main():
    board = Board(3)
    board.game()


if __name__ == "__main__":
    main()