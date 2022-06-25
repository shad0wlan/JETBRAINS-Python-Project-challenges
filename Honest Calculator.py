# write your code here
# variables declaration
msg_1 = "Do you even know what numbers are? Stay focused!"
msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"
msg_4 = "Do you want to store the result? (y / n):"
msg_5 = "Do you want to continue calculations? (y / n):"
msg_6 = " ... lazy"
msg_7 = " ... very lazy"
msg_8 = " ... very, very lazy"
msg_9 = "You are"
msg_10 = "Are you sure? It is only one digit! (y / n)"
msg_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"
msg_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"
operators = ["+", "-", "*", "/"]
calc = None
result = None
exit_calc = False
memory = 0
x = None
y = None


# Functions declaration


def is_one_digit(v):
    if -10 < v < 10 and float(v).is_integer():
        return True
    return False


def check(v1, v2, v3):
    msg = ""
    if is_one_digit(v1) and is_one_digit(v2):
        msg = msg + msg_6
    if (v1 == 1 or v2 == 1) and v3 == "*":
        msg = msg + msg_7
    if (v1 == 0 or v2 == 0) and (v3 == "*" or v3 == "+" or v3 == "-"):
        msg = msg + msg_8
    if msg != "":
        msg = msg_9 + msg

        print(msg)


while True:
    msg_0 = input("Enter an equation\n").strip().split()

    # Ensuring right equation length
    if len(msg_0) != 3:
        print("Wrong equation format")
        continue
    # Checking validity of inputs
    try:
        if msg_0[0] != "M":
            x = float(msg_0[0])
        elif msg_0[0] == "M":
            x = memory
        if msg_0[2] != "M":
            y = float(msg_0[2])
        elif msg_0[2] == "M":
            y = memory
    except ValueError:
        if msg_0[0].isalpha() or msg_0[2].isalpha():
            print(msg_1)
            continue
        elif not isinstance(msg_0[0], (float, int)) or not isinstance(msg_0[2], (float, int)):
            print(msg_1)
            continue
    if msg_0[1] not in operators:
        print(msg_2)
        continue
    else:
        oper = msg_0[1]
        
        if oper == "+":
            result = x + y
        elif oper == "-":
            result = x - y
        elif oper == "*":
            result = x * y
        else:
            if y == 0:
                check(x, y, oper)
                print("Yeah... division by zero. Smart move...")
                continue
            else:
                result = x / y
    check(x, y, oper)
    print(result)
    # Ensuring valid user input to store in memory or exit the program
    while True:
        answer = input(msg_4)
        if (answer == "y" or answer == "yes") and result >= 0:
            if is_one_digit(result):
                question = input(msg_10)
                if question == "y" or question == "yes":
                    question = input(msg_11)
                    if question == "y" or question == "yes":
                        question = input(msg_12)
                        if question == "y" or question == "yes":
                            memory = result
                            answer = input(msg_5)
                            if answer == "y" or answer == "yes":
                                break
                            elif answer == "n" or answer == "no":
                                answer = input(msg_5)
                                if answer == "y" or answer == "yes":
                                    break
                                elif answer == "n" or answer == "no":
                                    exit_calc = True
                                    break
                    elif question == "n" or question == "no":
                        answer = input(msg_5)
                        if answer == "y" or answer == "yes":
                            break
                        elif answer == "n" or answer == "no":
                            exit_calc = True
                            break
            else:
                memory = result
                answer = input(msg_5)
            if answer == "y" or answer == "yes":
                break
            elif answer == "n" or answer == "no":
                exit_calc = True
                break
        elif answer == "n" or answer == "no":
            answer = input(msg_5)
            if answer == "y" or answer == "yes":
                break
            elif answer == "n" or answer == "no":
                exit_calc = True
                break
        else:
            break
    if exit_calc:
        break
