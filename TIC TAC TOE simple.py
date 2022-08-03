# write your code here
MAX_ROUNDS = 9
empty_boxes = 9
game_on_progress = True

grid = [
    [" " for _ in range(3)],
    [" " for _ in range(3, 6)],
    [" " for _ in range(6, 9)]
]


def check_lines(w_grid):
    winning_lines = {
        "first_row": "".join(w_grid[0]),
        "second_row": "".join(w_grid[1]),
        "third_row": "".join(w_grid[2]),
        "first_column": w_grid[0][0] + w_grid[1][0] + w_grid[2][0],
        "second_column": w_grid[0][1] + w_grid[1][1] + w_grid[2][1],
        "third_column": w_grid[0][2] + w_grid[1][2] + w_grid[2][2],
        "first_diagonal": w_grid[0][0] + w_grid[1][1] + w_grid[2][2],
        "second_diagonal": w_grid[0][2] + w_grid[1][1] + w_grid[2][0]
    }
    return winning_lines.values()


def player_move(mark):
    global grid
    global empty_boxes
    while True:
        grid_position = input().strip().split(" ")
        try:
            grid_row = int(grid_position[0]) - 1
            grid_column = int(grid_position[1]) - 1
            if grid_row + 1 not in {1, 2, 3} or grid_column + 1 not in {1, 2, 3}:
                print("Coordinates should be from 1 to 3!")
                continue
            elif grid[grid_row][grid_column] in {"X", "O"}:
                print("This cell is occupied! Choose another one!")
                continue
            else:
                grid[grid_row][grid_column] = mark
                empty_boxes -= 1
                grid_print()
                return
        except ValueError:
            print("You should enter numbers!")


def check_winner(grids_to_check):
    global game_on_progress
    if "XXX" in grids_to_check:
        print("X wins")
        game_on_progress = False
        return True
    elif "OOO" in grids_to_check:
        print("O wins")
        game_on_progress = False
        return True
    elif empty_boxes < 1:
        print("Draw")
        game_on_progress = False
        return True


def grid_print():
    print("-" * (len(grid) * len(grid)))
    for i in grid:
        print("|", *i, "|")
    print("-" * (len(grid) * len(grid)))


def main():
    grid_print()
    while game_on_progress:
        game_round = 1
        player_move("X")
        check_winner(check_lines(grid))
        if game_on_progress:
            player_move("O")
            check_winner(check_lines(grid))
            game_round += 1



if __name__ == "__main__":
    main()

