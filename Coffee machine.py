# Write your code here
class CoffeeMachine:

    def __init__(self):
        self.materials = dict(water=400, milk=540, coffee_beans=120, money=550, cups=9)
        self.state = True
        self.coffee_types = {1: "espresso", 2: "latte", 3: "cappuccino"}
        self.coffee_requirements = {
            "espresso": {
                "water": 250,
                "coffee_beans": 16,
                "milk": 0,
                "money": 4,
                "cups": 1
            },
            "latte": {
                "water": 350,
                "milk": 75,
                "coffee_beans": 20,
                "money": 7,
                "cups": 1
            },
            "cappuccino": {
                "water": 200,
                "milk": 100,
                "coffee_beans": 12,
                "money": 6,
                "cups": 1
            }
        }



    def set_water(self, quantity):
        self.materials["water"] += quantity

    def get_water(self):
        return self.materials["water"]

    def set_milk(self, quantity):
        self.materials["milk"] += quantity

    def get_milk(self):
        return self.materials["milk"]

    def set_coffee_beans(self, quantity):
        self.materials["coffee_beans"] += quantity

    def get_coffee_beans(self):
        return self.materials["coffee_beans"]

    def set_cash(self, quantity):
        self.materials["cash"] += quantity

    def get_cash(self):
        return self.materials["cash"]

    def set_cups(self, quantity):
        self.materials["cups"] += quantity

    def get_cups(self):
        return self.materials["cups"]

    def buy(self, kind_of_coffee, cups_amount=1):
        try:
            coffee_choice = self.coffee_requirements[self.coffee_types[int(kind_of_coffee)]]
        except ValueError:
            print("Wrong input format - choose a correct index for coffee")
            return
        for i, j in coffee_choice.items():
            if self.materials[i] - (j * cups_amount) >= 0:
                if i == "money":
                    self.materials[i] += j
                else:
                    self.materials[i] -= j * cups_amount
            else:
                ingredient = i.replace("_", " ")
                print(f"Sorry, not enough {ingredient}!\n")
                return
        print("I have enough resources, making you a coffee!\n")

    def fill_machine(self, water_amount, milk_amount, beans_amount, cups_amount):
        self.set_water(water_amount)
        self.set_milk(milk_amount)
        self.set_coffee_beans(beans_amount)
        self.set_cups(cups_amount)

    def __str__(self):
        water_string = f'{self.materials["water"]} ml of water\n'
        milk_string = f'{self.materials["milk"]} ml of milk\n'
        beans_string = f'{self.materials["coffee_beans"]} g of coffee beans\n'
        cups_string = f'{self.materials["cups"]} disposable cups\n'
        money_string = f'${self.materials["money"]} of money\n'

        return f'The coffee machine has:\n{water_string + milk_string + beans_string + cups_string + money_string}'

    def take_money(self):
        earnings = self.materials["money"]
        self.materials["money"] -= earnings
        print(f"I gave you ${earnings}\n")
        return earnings

    def switch_state(self):
        if self.state:
            self.state = False
        else:
            self.state = True


machine = CoffeeMachine()
while machine.state:
    action_to_do = input("Write action (buy, fill, take, remaining, exit):\n").strip()
    if action_to_do in {"buy", "fill", "take", "remaining", "exit"}:
        if action_to_do == "buy":
            print()
            what_to_buy = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n")
            if what_to_buy == "back":
                continue
            else:
                coffee = int(what_to_buy)
                machine.buy(coffee)
                continue
        elif action_to_do == "fill":
            print()
            try:
                water = int(input("Write how many ml of water you want to add:\n"))
                milk = int(input("Write how many ml of milk you want to add:\n"))
                beans = int(input("Write how many grams of coffee beans you want to add:\n"))
                cups = int(input("Write how many disposable cups you want to add:\n"))
                machine.fill_machine(water, milk, beans, cups)
                print()
                continue
            except ValueError as f:
                print(f"Wrong input value in {f}")
                continue
        elif action_to_do == "remaining":
            print()
            print(machine)
            continue
        elif action_to_do == "take":
            print()
            machine.take_money()
            continue
        else:
            machine.switch_state()
    else:
        print("Wrong action")


