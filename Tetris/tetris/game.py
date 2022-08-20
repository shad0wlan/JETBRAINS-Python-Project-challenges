# Write your code here
import numpy as np
from copy import deepcopy
from collections import deque


class Tetris:


    def __init__(self, w_size, h_size):
        self.w_size = w_size
        self.h_size = h_size
        self.w = self.w_size
        self.dimensions = w_size * h_size
        self.board = np.arange(self.dimensions).reshape((h_size, w_size))
        self.board_play = np.array(['-' for _ in range(self.dimensions)], dtype=str).reshape((h_size, w_size))

        self.O = [[(self.w - 1) // 2, (self.w - 1) // 2 + 1, (self.w - 1) // 2 + self.w, (self.w - 1) // 2 + self.w + 1]] * 4

        self.I = [[(self.w - 1) // 2, (self.w - 1) // 2 + self.w, (self.w - 1) // 2 + self.w * 2, (self.w - 1) // 2 + self.w * 3],
             [(self.w - 1) // 2 - 1, (self.w - 1) // 2, (self.w - 1) // 2 + 1, (self.w - 1) // 2 + 2]] * 2

        self.S = [[(self.w - 1) // 2, (self.w - 1) // 2 + 1, (self.w - 1) // 2 + self.w - 1, (self.w - 1) // 2 + self.w],
             [(self.w - 1) // 2, (self.w - 1) // 2 + self.w, (self.w - 1) // 2 + self.w + 1, (self.w - 1) // 2 + self.w * 2 + 1]] * 2

        self.Z = [[(self.w - 1) // 2, (self.w - 1) // 2 + 1, (self.w - 1) // 2 + 1 + self.w, (self.w - 1) // 2 + self.w + 2],
             [(self.w - 1) // 2 + 1, (self.w - 1) // 2 + self.w, (self.w - 1) // 2 + self.w + 1, (self.w - 1) // 2 + self.w * 2]] * 2

        self.L = [[(self.w - 1) // 2, (self.w - 1) // 2 + self.w, (self.w - 1) // 2 + self.w * 2, (self.w - 1) // 2 + self.w * 2 + 1],
             [(self.w - 1) // 2 + 1, (self.w - 1) // 2 + self.w - 1, (self.w - 1) // 2 + self.w, (self.w - 1) // 2 + self.w + 1],
             [(self.w - 1) // 2, (self.w - 1) // 2 + 1, (self.w - 1) // 2 + self.w + 1, (self.w - 1) // 2 + self.w * 2 + 1],
             [(self.w - 1) // 2, (self.w - 1) // 2 + 1, (self.w - 1) // 2 + 2, (self.w - 1) // 2 + self.w]]

        self.J = [[(self.w - 1) // 2 + 1, (self.w - 1) // 2 + self.w + 1, (self.w - 1) // 2 + self.w * 2,
              (self.w - 1) // 2 + self.w * 2 + 1],
             [(self.w - 1) // 2 - 1, (self.w - 1) // 2, (self.w - 1) // 2 + 1, (self.w - 1) // 2 + self.w + 1],
             [(self.w - 1) // 2, (self.w - 1) // 2 + 1, (self.w - 1) // 2 + self.w, (self.w - 1) // 2 + self.w * 2],
             [(self.w - 1) // 2, (self.w - 1) // 2 + self.w, (self.w - 1) // 2 + self.w + 1, (self.w - 1) // 2 + self.w + 2]]

        self.T = [[(self.w - 1) // 2, (self.w - 1) // 2 + self.w, (self.w - 1) // 2 + self.w + 1, (self.w - 1) // 2 + self.w * 2],
             [(self.w - 1) // 2, (self.w - 1) // 2 + self.w - 1, (self.w - 1) // 2 + self.w, (self.w - 1) // 2 + self.w + 1],
             [(self.w - 1) // 2 + 1, (self.w - 1) // 2 + self.w, (self.w - 1) // 2 + self.w + 1, (self.w - 1) // 2 + self.w * 2 + 1],
             [(self.w - 1) // 2, (self.w - 1) // 2 + 1, (self.w - 1) // 2 + 2, (self.w - 1) // 2 + self.w + 1]]

        self.bricks_mapping = {"O": np.array(self.O),
                               "I": np.array(self.I),
                               "S": np.array(self.S),
                               "Z": np.array(self.Z),
                               "L": np.array(self.L),
                               "J": np.array(self.J),
                               "T": np.array(self.T)}
        self.bricks_mapping_duplicate = deepcopy(self.bricks_mapping)
        self.rotations = {"left": -1, "down": 10, "right": 1}
        self.board_frozen_state = np.array([False for _ in range(self.dimensions)]).reshape((h_size, w_size))
        self.frozen_moves = deque()  # A variable to hold the moves that are static
        self.is_over = False
        self.current_move = None
        self.current_move_whole = None

    def bricks(self, shape_type, rotation=None):
        board_play_duplicate = np.where(self.board_frozen_state, "0", "-")
        self.current_move = self.bricks_mapping[shape_type][0]
        self.current_move_whole = self.bricks_mapping[shape_type]

        try:
            if self.brick_collision(self.current_move, board_play_duplicate):
                print(self.__str__())
                return False

            if self.bottom_end_check(self.current_move, board_play_duplicate):
                print(self.__str__())
                return False

            if rotation in self.rotations.keys():
                collision = self.board_collision(self.current_move_whole, self.current_move, rotation)
                if not collision:
                    self.current_move_whole += self.rotations[rotation] + 10

            if rotation == "rotate":
                deq_manipulation = deque(self.current_move_whole)
                deq_manipulation.append(deq_manipulation.popleft())
                self.bricks_mapping[shape_type] = np.array(deq_manipulation) + 10
                self.current_move = self.bricks_mapping[shape_type][0]

            self.bottom_end_check(self.current_move, board_play_duplicate)

            for i in self.current_move:
                board_play_duplicate[self.board == i] = "0"
            for k in board_play_duplicate:
                print(*k)
            print()

        except KeyError:
            return 'Wrong brick value'

    # Reset all moves state when choose other piece
    def move_reset(self):
        self.bricks_mapping = deepcopy(self.bricks_mapping_duplicate)

    # Checking edges collision
    def board_collision(self, shape, move, direction):
        if (np.any(np.in1d(move, self.board[:, 0])) and direction == "left") or \
                (np.any(np.in1d(move, self.board[:, -1])) and direction == "right") or direction == "down":
            shape += self.rotations["down"]
            return True
        return False

    # Checking ending board
    def bottom_end_check(self, move, board):
        if np.any(np.in1d(move, self.board[-1, :])):
            if list(move) not in self.frozen_moves:
                self.frozen_moves.append(list(move))
            for i in move:
                self.board_frozen_state[self.board == i] = True
                board[self.board_frozen_state] = "0"
            return True

    # Checking bricks collision(the move is registered on the same round (i + 10))
    def brick_collision(self, move, board):
        for i in move:
            if np.any(np.in1d(i + 10, self.frozen_moves)):
                if list(move) not in self.frozen_moves:
                    self.frozen_moves.append(list(move))
                for j in move:
                    self.board_frozen_state[self.board == j] = True
                board[self.board_frozen_state] = "0"
                return True
        return False

    # Refreshing board after each movement by reading the True fields of the helper self.board_state
    def board_refresher(self):
        self.board_play = np.where(self.board_frozen_state, "0", "-")

    # Checking if any column leads to game over
    def check_game_over(self):
        for i in range(self.board_frozen_state.shape[1]):
            if np.alltrue(self.board_frozen_state[:, i]):
                self.is_over = True
                return True

    # Checking if any row is valid for breaking / each row is breaking individually
    def board_break(self):
        for i in range(self.board_frozen_state.shape[0]):
            if np.alltrue(self.board_frozen_state[-1, :]):
                new_row = np.array([False for _ in range(self.w_size)])
                self.board_frozen_state = np.insert(self.board_frozen_state, 0, new_row, axis=0)
                self.board_frozen_state = np.delete(self.board_frozen_state, -1, axis=0)
                image = self.board[-1, :]
                frozen_moves_editor = np.array(self.frozen_moves, dtype=object)
                frozen_moves_editor[np.isin(frozen_moves_editor, image)] = -1
                frozen_moves_editor = frozen_moves_editor[~np.all(frozen_moves_editor == -1, axis=1)]
                frozen_moves_editor += 10
                self.frozen_moves = deque([list(i) for i in frozen_moves_editor])

    def __str__(self):
        self.board_play = np.where(self.board_frozen_state, "0", "-")
        representation = (str(self.board_play).replace(' [', '').replace('[', '').replace(']', '')).replace("'", '')
        return representation + "\n"


def main():
    while True:
        try:
            dimensions = input().split()
            width = int(dimensions[0])
            height = int(dimensions[1])
            new_game = Tetris(width, height)
            print(new_game)
            break
        except IndexError:
            print("Enter correct dimensions")
            continue

    while not new_game.is_over:
        action = input().lower()
        brick = input().upper()
        new_game.bricks(brick)
        while not new_game.is_over:
            x = input()
            if new_game.check_game_over():
                print(new_game)
                print("Game Over!")
                break
            if x in {"left", "right", "down", "rotate", "piece", "break", "exit"}:
                if x == "piece":
                    new_game.move_reset()
                    brick = input().upper()
                if x == "break":
                    new_game.board_break()
                    print(new_game)
                    continue
                if x == "exit":
                    new_game.is_over = True
                    break
                new_game.bricks(brick, x)

            else:
                print("Wrong input")


if __name__ == "__main__":
    main()
