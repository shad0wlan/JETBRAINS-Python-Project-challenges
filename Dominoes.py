# Write your code here
from random import randrange


length = 28
first_player = None
end = False
domino_snake = []

# Must import shuffle if we go through this set generator and indent lines
# def set_generator():
# dominos = [(i, j) for i in range(7) for j in range(i,7)]
# print(dominos)
# shuffle(dominos)
# return dominos

# Using a function with set for training in sets as another way to reproduce the same result


def unique_set_generator(set_size):
    unique_set = set()
    main_set = []
    while len(unique_set) != set_size:
        x, y = randrange(7), randrange(7)
        if (x, y) not in unique_set and (y, x) not in unique_set:
            unique_set.add((x, y))
    set_to_list = list(unique_set)

    for i in range(set_size):
        main_set.append(list(set_to_list[i]))

    return main_set


def random_split(main_list, split_length, main_list_for_random_index, target_list):
    # The swap below is used to avoid O(n) behavior on deletion from a middle of a list we also could shuffle but this
    # increases time in large sets.

    for i in range(split_length):
        random_index = randrange(len(main_list_for_random_index))
        main_list[random_index], main_list[-1] = main_list[-1], main_list[random_index]
        target_list.append(main_list.pop())


# Evaluating First player
def starting_piece(player_one, player_two):
    global domino_snake
    global first_player
    player_one_doubles = [player_one[i] for i in range(len(player_one)) if player_one[i][0] == player_one[i][1]]
    player_two_doubles = [player_two[i] for i in range(len(player_two)) if player_two[i][0] == player_two[i][1]]
    max_player_one = []
    max_player_two = []
    if len(player_one_doubles) > 0:
        max_player_one = max(player_one_doubles)
    if len(player_two_doubles) > 0:
        max_player_two = max(player_two_doubles)

    if max_player_one > max_player_two:
        first_player = "computer"
        player_one.pop(player_one.index(max_player_one))
        domino_snake = [max_player_one]
        return True
    if max_player_one < max_player_two:
        first_player = "player"
        domino_snake = [max_player_two]
        player_two.pop(player_two.index(max_player_two))
        return True
    else:
        return False


def player_printer(player_list):

    print("Your pieces:")
    for i in range(len(player_list)):
        print(f'{i + 1}: {player_list[i]}')


def round_printer(stock_set, computer_set, player_set, snake_set):
    print("=" * 70)
    print(f'Stock size: {len(stock_set)}')
    print(f'Computer pieces: {len(computer_set)}')
    print()
    if len(snake_set) >= 6:
        print(*snake_set[:3], "...", *snake_set[-3:], sep='')

    else:
        for i in range(len(snake_set)):
            print(snake_set[i], end="")
        print()

    print()
    player_printer(player_set)


def player_move(player_set, computer_set,  stock_set, snake_set):
    global end
    if end_game(player_set, computer_set, snake_set, stock_set):
        end = True
        return
    x = input("Status: It's your turn to make a move. Enter your command.\n")

    while True:
        if x.lstrip("-").isdigit():
            y = int(x)
            if abs(y) - 1 >= len(player_set):
                print("Invalid input. Please try again.")
                x = input()
                continue
            if y > 0 and y - 1 < len(player_set):
                player_choice = player_set[y - 1]
                if player_choice[0] == snake_set[-1][1]:
                    snake_set.append(player_set.pop(y - 1))
                elif player_choice[1] == snake_set[-1][1]:
                    snake_set.append(list(reversed(player_set.pop(y - 1))))
                else:
                    print("Illegal move. Please try again.")
                    x = input()
                    continue
            elif y < 0 and abs(y) - 1 < len(player_set):
                player_choice = player_set[abs(y) - 1]
                if player_choice[0] == snake_set[0][0]:
                    snake_set.insert(0, list(reversed(player_set.pop(abs(y) - 1))))
                elif player_choice[1] == snake_set[0][0]:
                    snake_set.insert(0, player_set.pop(abs(y) - 1))
                else:
                    print("Illegal move. Please try again.")
                    x = input()
                    continue
            else:
                player_set.append(stock_set.pop(randrange(0, len(stock_set))))
        else:
            print("Invalid input. Please try again.")
            x = input()
            continue
        round_printer(stock_set, computer_set, player_set, snake_set)
        break


def computer_move(computer_set, player_set, stock_set, snake_set):
    global end
    if end_game(player_set, computer_set, snake_set, stock_set):
        end = True
        return
    input("Status: Computer is about to make a move. Press Enter to continue...")
    combined_list = computer_set + snake_set
    numbers_summary = {}
    for i in combined_list:
        for k in i:
            numbers_summary[k] = numbers_summary.get(k, 0) + 1
    sum_of_pairs = {}
    for i in computer_set:
        sum_of_pairs[tuple(i)] = numbers_summary[i[0]] + numbers_summary[i[1]]

    scores = {key: value for key, value in reversed(sorted(sum_of_pairs.items(), key=lambda item: item[1]))}
    computer_choices = list(scores.keys())
    for i in computer_choices:
        index_for_i = computer_set.index(list(i))
        if i[0] == snake_set[-1][1]:
            snake_set.append(computer_set.pop(index_for_i))
            break
        elif i[1] == snake_set[-1][1]:
            snake_set.append(list(reversed(computer_set.pop(index_for_i))))
            break
        elif i[0] == snake_set[0][0]:
            snake_set.insert(0, list(reversed(computer_set.pop(index_for_i))))
            break
        elif i[1] == snake_set[0][0]:
            snake_set.insert(0, computer_set.pop(index_for_i))
            break
        elif index_for_i == len(computer_choices) - 1:
            computer_set.append(stock_set.pop(randrange(0, len(stock_set))))
            break
    round_printer(stock_set, computer_set, player_set, snake_set)


def end_game(player_set, computer_set, snake_set, stock_set):

    if len(player_set) == 0:
        print("\nStatus: The game is over. You won!")
        return True
    if len(computer_set) == 0:
        print("\nStatus: The game is over. The computer won!")
        return True
    if snake_set[0][0] == snake_set[-1][1] and len(snake_set) >= 7:
        cnt = 0
        for i in snake_set:
            for j in i:
                if snake_set[0][0] == j:
                    cnt += 1

        if cnt == 8:
            print("\nStatus: The game is over. It's a draw!")
            return True
    if len(stock_set) == 0:
        print("\nStatus: The game is over. It's a draw!")
        return True
    return False


def main():
    global domino_snake
    global end
    full_set = unique_set_generator(length)
    stock_pieces = []
    player_set = []
    computer_set = []
    random_split(full_set, length // 4, full_set, player_set)
    random_split(full_set, len(full_set) // 3, full_set, computer_set)
    random_split(full_set, len(full_set), full_set, stock_pieces)
    while not end:
        if starting_piece(player_set, computer_set):
            round_printer(stock_pieces, computer_set, player_set, domino_snake)
            while True:
                if end:
                    break
                if first_player == "player":
                    player_move(player_set, computer_set, stock_pieces, domino_snake)
                    if end:
                        break
                    computer_move(computer_set, player_set, stock_pieces, domino_snake)

                elif first_player == "computer":
                    computer_move(computer_set, player_set, stock_pieces, domino_snake)
                    if end:
                        break
                    player_move(player_set, computer_set, stock_pieces, domino_snake)

        else:
            continue


if __name__ == "__main__":
    main()
