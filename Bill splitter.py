# write your code here
from random import choice
valid_invitation = False
lucky_feature = False
bill_value = 0


def friend_invite():
    global valid_invitation
    while True:
        try:
            number_of_friends = int(input("Enter the number of friends joining (including you):\n"))
            if number_of_friends <= 0:
                return 'No one is joining for the party'
            break
        except ValueError:
            print("Only numeric values allowed")
    print("Enter the name of every friend (including you), each on a new line:\n")

    friends = {input(): 0 for _ in range(number_of_friends)}
    valid_invitation = True
    return friends


def bill_split(dictionary_to_parse, lucky_person=None):
    global bill_value
    names = dictionary_to_parse.keys()
    while True:
        try:
            total_bill = int(input("Enter the total bill value:\n"))
            if total_bill <= 0:
                return 'Cant split inputted bill value'
            break
        except ValueError:
            print("Only numeric values allowed")
    bill_for_each_friend = round(total_bill / len(dictionary_to_parse), 2)
    bill_value = total_bill
    for i in names:
        dictionary_to_parse[i] = bill_for_each_friend

    return dictionary_to_parse

def lucky_split(dictionary_to_parse, name):
    global bill_value
    names = dictionary_to_parse.keys()
    bill_for_each_friend = round(bill_value / (len(dictionary_to_parse) - 1), 2)
    for i in names:
        if i == name:
            dictionary_to_parse[i] = 0
        else:
            dictionary_to_parse[i] = bill_for_each_friend
    print(dictionary_to_parse)


def who_is_lucky(dictionary_to_parse):
    global lucky_feature
    lucky_question = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n')
    if lucky_question.lower() == "yes":
        x = choice(list(dictionary_to_parse.keys()))
        lucky_feature = True
        print(f'{x} is the lucky one!\n\n')
        return x
    else:
        return 'No one is going to be lucky'


invitation = friend_invite()
if valid_invitation:
    print()
    split = bill_split(invitation)
    print()
    lucky = who_is_lucky(split)
    if not lucky_feature:
        print(lucky)
        print()
        print(split)
    else:
        final_split = lucky_split(split, lucky)
else:
    print(invitation)
