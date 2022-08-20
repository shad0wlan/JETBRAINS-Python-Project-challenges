# Write your code here
from copy import deepcopy
import sys
sys.setrecursionlimit(2000)
# With that recursion limit you can test boards up to 40x40 instantly.
# Without this you can test easily up to 30 x 30 any value
# and up to 35x35 any value except edge columns / rows ex 1 4 / 4 1.


class ChessBoard:

    def __init__(self, dimensions: str):
        self.game_over = False
        self.valid_grid = True
        self.dimensions = self.board_validation(dimensions.strip().split())
        if self.valid_grid:
            self.x = self.dimensions[0]
            self.y = self.dimensions[1]
            self.cell_length = len(str(self.x * self.y))  # Cell format helper for spaces
            self.board = [[(x, y) for x in range(1, self.x + 1)] for y in range(self.y, 0, -1)]
            self.visual = [["_" * self.cell_length for _ in range(1, self.x + 1)] for _ in range(self.y, 0, -1)]
            self.moves_visit = {key: False for i in range(len(self.board)) for key in self.board[i]}

            # We need duplicates to reverse the state of the board if we want:
            # to continue the game - try other initial move for the valid movements pool
            self.board_duplicate = deepcopy(self.board)
            self.visual_duplicate = deepcopy(self.visual)
            self.moves_visit_duplicate = deepcopy(self.moves_visit)

            self.x_boundaries = {i for i in range(1, self.x + 1)}
            self.y_boundaries = {i for i in range(1, self.y + 1)}
            self.valid_moves = []  # Helper for getting instant valid_moves for the player.
            self.is_first_move = True  # With that we make it easier to differentiate the first move from other inputs.
            self.movements_made = 0  # Move counter direct connection with the AI solution finder and the AI move
            self.board_dimensions = self.x * self.y
            self.has_solution = False
            self.initial_move_for_ai = None
            self.first_valid_move = set({})
            self.moves_placed = set({})  # Fast comparison to check if the ai_play function will return from recursion
            self.total_moves = 0
            self.find_solution_mode = False

    def set_first(self):
        if self.is_first_move:
            self.is_first_move = False

    def board_validation(self, board_dimensions):
        if len(board_dimensions) != 2:
            self.valid_grid = False
            return False
        try:
            x = int(board_dimensions[0])
            y = int(board_dimensions[1])
            if x <= 0 or y <= 0:
                self.valid_grid = False
                return False
            self.valid_grid = True
            return x, y
        except ValueError:
            self.valid_grid = False
            return False

    def move_validation(self, move_to_validate):
        if isinstance(move_to_validate, tuple) and move_to_validate[0] in self.x_boundaries and \
                move_to_validate[1] in self.y_boundaries:
            return move_to_validate
        values = move_to_validate.split()
        if len(values) != 2:
            return False
        try:
            column = int(values[0])
            row = int(values[1])
            movement = (column, row)
            if column not in self.x_boundaries or row not in self.y_boundaries:
                return False
            if not self.is_first_move and self.moves_visit[movement]:
                return False
            if not self.is_first_move and movement not in self.valid_moves:
                return False
            return movement
        except ValueError:
            return False

    # Knight movement. X for player - Movement number for AI
    def knight_move(self, movement, solution_mode=False):
        if self.movements_made == 0:
            self.set_first()
        movement = self.move_validation(movement)
        for m in range(len(self.board)):
            if movement in self.board[m]:
                index_of_move = self.board[m].index(movement)
                if not self.moves_visit[movement]:
                    if not solution_mode:
                        self.visual[m][index_of_move] = " " * (self.cell_length - 1) + "X"
                    else:
                        move = "" * (self.cell_length - 3) + str(self.movements_made + 1)
                        self.visual[m][index_of_move] = move.rjust(self.cell_length)
                    self.possible_moves(movement)
                    self.movements_made += 1
                    self.moves_visit[movement] = True
                return movement
        return False

    # Calculating exact moves to chose from. We return index based values based on visual repr
    # and also player based values (2, 1), (3, 2) etc.. columns / rows
    def move_calculation(self, movement_to_calc):
        movement = movement_to_calc
        value_to_process = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (-1, -2), (1, -2)]
        possible_calculations = [(movement[0] + value_to_process[i][0], movement[1] +
                                  value_to_process[i][1]) for i in range(len(value_to_process))]

        final_possible_indexes = [(r, self.board[r].index(j)) for r in range(len(self.board))
                                  for j in possible_calculations if j in self.board[r] and not self.moves_visit[j]]

        final_possible_indexes_translation = [self.board[i][j] for i, j in final_possible_indexes]

        return final_possible_indexes, final_possible_indexes_translation

    # Function that is used to calculate how many moves we have for the valid placements on board
    def depth_calc(self, valid_move):
        x, y = self.move_calculation(valid_move)
        return len(x)

    # Similar to move_calculation but this one is used to register primary valid moves for player on board
    # And also to check the state of players game and outputting the depth values for the valid moves.
    def possible_moves(self, main_move):
        try:
            moves, moves_translation = self.move_calculation(main_move)
            combined_index_translation = set(zip(moves, moves_translation))
        except TypeError:
            return False

        if not self.find_solution_mode:
            for i, j in combined_index_translation:
                col, row = i[0], i[1]
                if not self.moves_visit[j]:
                    self.visual[col][row] = f'{" " * (self.cell_length - 1)}{self.depth_calc(j) - 1}'
            self.valid_moves = moves_translation
            print(self.__str__())
            self.board_updater()
            self.check_end()
        return moves_translation

    # Board update based on the moves_visit state True/False (if we visited or not)
    def board_updater(self):

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                move_to_check = self.board[i][j]
                if self.moves_visit[move_to_check]:
                    self.visual[i][j] = f'{" " * (self.cell_length - 1)}*'
                else:
                    self.visual[i][j] = f'{" " * (self.cell_length - 1)}_'

    # Getting all primary valid moves to work with
    def get_valid_moves(self, from_move):
        valid = self.possible_moves(from_move)
        if valid:
            return valid
        else:
            return False

    # Key function for the ai_play function. It gives us the valid move with the minimum depth.
    def lower_move(self, valid_values):
        lengths = {i: self.depth_calc(i) for i in valid_values}
        min_depth = min(lengths, key=lengths.get)
        return min_depth

    # Recursive function that is giving us the solution for the inputted move
    def ai_play(self, move, pool, n):

        if not self.moves_placed:
            self.moves_placed.add(move)
        if n == 1:
            self.first_valid_move.add(self.lower_move(pool))
        if len(self.moves_placed) == self.board_dimensions:
            self.has_solution = True
            return True
        if self.total_moves >= self.board_dimensions ** 4:
            return False

        self.total_moves += 1

        if pool:
            best_move = self.lower_move(pool)
            ai_move = self.knight_move(best_move, solution_mode=True)
            self.moves_placed.add(ai_move)
            if ai_move:
                possible_moves = self.get_valid_moves(ai_move)
                if self.ai_play(ai_move, possible_moves, n + 1):
                    return True
        else:
            self.ai_play_reset()
            first_move = self.knight_reset()
            self.moves_placed.add(first_move)
            first_pool = self.get_valid_moves(first_move)
            self.first_valid_move.add(first_pool[0])
            new_pool = set(first_pool).difference(self.first_valid_move)
            try:
                self.ai_play(first_move, list(new_pool), 1)
            except RecursionError:
                self.ai_play_reset()
                return False
            except IndexError:
                print("We tested all initial valid moves and failed.\nChoose one cell higher column and try again")
                return False

    # Resets the important variables of the board. Crucial if ai_play doesn't find a solution with first try.
    def ai_play_reset(self):
        self.moves_placed.clear()
        self.board = deepcopy(self.board_duplicate)
        self.visual = deepcopy(self.visual_duplicate)
        self.moves_visit = deepcopy(self.moves_visit_duplicate)
        self.movements_made = 0
        self.has_solution = False
        self.first_valid_move.clear()

    # Checks the state of the player's game.
    def check_end(self):
        if not self.valid_moves:
            self.game_over = True
            if self.movements_made + 1 == self.board_dimensions:
                self.has_solution = True
                print("What a great tour! Congratulations!")
                return False
            else:
                print(f"No more possible moves!\nYour knight visited {self.movements_made + 1} squares!")
            return False

    # Resets the Knight position to the initial for the ai_play function
    def knight_reset(self):
        main_move = self.knight_move(self.initial_move_for_ai, solution_mode=True)
        return main_move

    # Helper function that manages the outputs of the ai_play function regarding if player want a solution or not
    def ai_solution_test(self, move, for_player=False):
        if self.board_dimensions in {16, 4, 9}:
            print("No solution exists!")
            return False
        self.initial_move_for_ai = move
        self.find_solution_mode = True
        movement = self.knight_move(move, solution_mode=True)
        self.set_first()
        self.initial_move_for_ai = movement
        valid_moves = self.get_valid_moves(movement)
        while True:
            self.ai_play(movement, valid_moves, 1)
            if self.has_solution:
                if not for_player:
                    print("\nHere's the solution!")
                    print(self.__str__())
                    break
                else:
                    break
        self.find_solution_mode = False
        self.ai_play_reset()
        return True

    def __str__(self):
        visualization = [" ".rjust(self.cell_length - 1) + "-" * (self.x * (self.cell_length + 1) + 3)]
        for i in range(len(self.visual)):
            main_chess = " ".join([str(len(self.visual) - i).rjust(self.cell_length - 1) + "|", *self.visual[i], "|"])
            visualization.append(main_chess)
        visualization.append(" " * (self.cell_length - 1) + "-" * (self.x * (self.cell_length + 1) + 3))
        visualization.append(
            " ".rjust(self.cell_length + 2) + " ".join([f"{i}".center(self.cell_length) for i in range(1, self.x + 1)]))
        return "\n".join(visualization)


def main():
    while True:
        board = ChessBoard(input("Enter your board's dimensions: "))
        if not board.valid_grid:
            print("Invalid dimensions!", end=" ")
            continue
        while True:
            knight_move = board.move_validation(input("Enter the knight's starting position: "))
            if not knight_move:
                print("Invalid move!", end=" ")
                continue
            else:
                break
        while True:
            puzzle_try = input("Do you want to try the puzzle? (y/n): ")
            if puzzle_try not in {"y", "n"}:
                print("Invalid input!", end=" ")
                continue
            else:
                break
        if puzzle_try == "y":
            check_if_solution = board.ai_solution_test(knight_move, for_player=True)
            if check_if_solution:
                board.knight_move(knight_move)
                while not board.game_over:
                    next_move = board.knight_move(input("Enter your next move: "))
                    if next_move:
                        board.board_updater()
                    else:
                        print("Invalid move!", end=" ")
                        continue
                    if board.game_over:
                        break
            else:
                break
        else:
            board.ai_solution_test(knight_move)
        break


if __name__ == "__main__":
    main()
