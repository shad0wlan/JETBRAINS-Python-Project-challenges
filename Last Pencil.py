from random import randrange

x = 0
players = ["John", "Jack"]
first_player = None
second_player = None
we_have_winner = False
player_choice = None
bot_choice = None


def is_valid_input(num):
    global we_have_winner
    global x
    if num not in ["1", "2", "3"]:
        print("Possible values: '1', '2' or '3'")
        return False
    if num.isdigit() and int(num) > x:
        print("Too many pencils were taken")
        return False
    if int(num) - x == 0:
        we_have_winner = True
        return True
    return int(num)


# Checking valid number for initial pencils
def initial_pencils_validator():
    global x
    x = input("How many pencils would you like to use:\n")
    while True:
        try:
            if int(x) > 0:
                x = int(x)
                return True
            elif int(x) <= 0:
                print("The number of pencils should be positive")
                x = input()
                continue
        except ValueError:
            print("The number of pencils should be numeric")
            x = input()
            continue

# Validate name input


def name_validator():
    global players
    global first_player
    global second_player
    name = input("Who will be the first (John, Jack)\n")
    while True:
        if name not in players:
            print("Choose between 'John' and 'Jack'")
            name = input()
            continue
        else:
            if name == players[0]:
                first_player, second_player = players[0], players[1]
            else:
                first_player, second_player = players[1], players[0]
        return


def name_printer():
    if first_player == players[0]:
        print(f'{players[0]} turn:')

    elif first_player == players[1]:
        print(f'{players[1]} turn:')


def game_name_printer(player):
    print(f'{player} turn:')


def bot_move():
    global x
    global we_have_winner
    global bot_choice

    if x % 4 == 0:
        bot_choice = 3
        x -= 3
        return True
    elif x % 4 == 3:
        bot_choice = 2
        x -= 2
        return True
    elif x % 4 == 2:
        bot_choice = 1
        x -= 1
        return True
    elif x == 1:
        bot_choice = 1
        x -= 1
        we_have_winner = True
        return True
    else:
        bot_choice = randrange(1, 4)
        x -= bot_choice


def pencils_printer():
    print("|" * x)


def player_move():
    global x
    global player_choice
    while True:
        pencils_amount = input()
        if is_valid_input(pencils_amount):
            x -= int(pencils_amount)
            if round == 1:
                player_choice = int(pencils_amount)
            break
        continue


def is_winner_printer(player):
    if x == 0:
        print(f'{player} won!')
        return True
    return False


initial_pencils_validator()
name_validator()
print("|" * x)
name_printer()

while x > 0:
    # Jacks logic 1st player
    if first_player == players[1]:
        bot_move()
        print(bot_choice)
        if we_have_winner:
            is_winner_printer(second_player)
            break
        pencils_printer()
        game_name_printer(second_player)
        player_move()
        if we_have_winner:
            is_winner_printer(first_player)
            break
        pencils_printer()
        game_name_printer(first_player)

    # Player 1st player logic
    elif first_player == players[0]:
        player_move()
        if we_have_winner:
            is_winner_printer(second_player)
            break
        pencils_printer()
        game_name_printer(second_player)
        bot_move()
        print(bot_choice)
        if we_have_winner:
            is_winner_printer(first_player)
            break
        pencils_printer()
        game_name_printer(first_player)
