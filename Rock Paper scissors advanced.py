# Write your code here
#if you want to auto create file just add a+ / w+ mode to file mode

from random import choice


def player_input():
    move = input()
    if move in OPTIONS:
        return OPTIONS[OPTIONS.index(move)]
    else:
        return move


def computer_move():
    return choice(OPTIONS)


def decide_result(player_move, list_to_check):
    temp_list = list_to_check
    working_value = temp_list[player_move]
    other_list = temp_list[player_move:] + temp_list[:player_move]
    other_list.remove(working_value)
    losing_to_list = other_list[: len(other_list) // 2]
    return losing_to_list


name = input("Enter your name: ")
print(f"Hello, {name}")
play_input_list = input().split(",")
if len(play_input_list) <= 1:
    OPTIONS = ["rock", "paper", "scissors"]
else:
    OPTIONS = play_input_list
rating = 0
print("Okay, let's start")
with open("rating.txt") as f:
    for line in f:
        if line.startswith(name):
            rating += int(line.strip().split(" ")[1])

while True:
    player = player_input()
    if player == "!exit":
        print("Bye!")
        break
    if player == "!rating":
        print(f'Your rating: {rating}')
        continue
    if player in OPTIONS:
        computer = computer_move()
        player_index = OPTIONS.index(player)
        computer_index = OPTIONS.index(computer)
        result = decide_result(player_index, OPTIONS)
        if computer_index == player_index:
            print(f'There is a draw ({player})')
            rating += 50
            continue
        if computer in result and OPTIONS[player_index] not in result:
            print(f'Sorry, but the computer chose {computer}')
            continue
        else:
            print(f'Well done. The computer chose {computer} and failed')
            rating += 100
            continue
    else:
        print("Invalid input")
