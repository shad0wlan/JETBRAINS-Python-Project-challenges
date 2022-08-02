# write your code here
# Tic tac toe independent of size. For example if we create instance with parameter 5,
# It will create a Board object with 5x5 dimensions, entering 6 will create 6x6 etc.
# In order to win, players mark in correct line must be equal to board's dimension (ex XXXXX/OOOOO)

class Board:
    def __init__(self, dimension):
        self.dimension = dimension
        self.grid = [[f" " for _ in range(dimension)] for _ in range(1, dimension + 1)]
        self.empty_boxes = dimension * dimension
        self.length = (dimension * 2) + 3
        self.state = True
        self.valid_values = [i for i in range(dimension)]
        self.max_value = max(self.valid_values) + 1
        print(self.__str__())

    def check_grid_values(self, grid=None):
        if grid is None:
            grid = self.grid
        winning_lines = {}
        for i in range(len(grid)):
            winning_lines[f'Row: {i + 1}'] = "".join(grid[i])
            winning_lines[f'Column: {i + 1}'] = "".join([grid[j][i] for j in range(len(grid))])

        winning_lines[f'Diagonal: 1'] = "".join([grid[i][i] for i in range(len(grid))])
        winning_lines[f'Diagonal: 2'] = "".join([grid[i][(len(grid) - 1) - i] for i in range(len(grid))])
        return winning_lines.values()

    def check_valid_move(self, move, player):
        if len(move) <= 1:
            print("Enter row/column values separated with space.")
            return False
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

    def check_winner(self):
        grid_values = self.check_grid_values()
        if "X" * self.dimension in grid_values:
            print("X wins")
            self.state = False
            return True
        elif "O" * self.dimension in grid_values:
            print("O wins")
            self.state = False
            return True
        elif self.empty_boxes < 1:
            print("Draw")
            self.state = False
            return True

    def game(self):
        while self.state:
            player_1 = "X"
            player_2 = "O"
            p1_move = input().strip().split()
            if not self.check_valid_move(p1_move, player_1):
                continue
            self.check_winner()
            if not self.state:
                break
            p2_move = input().strip().split()
            if not self.check_valid_move(p2_move, player_2):
                continue
            self.check_winner()

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
