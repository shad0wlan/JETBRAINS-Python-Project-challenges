# write your code here
from collections import defaultdict
import re


class Calculator:
    def __init__(self):
        self._calculations = {
            '+': self.addition,
            '-': self.subtraction,
            '*': self.multiplication,
            '/': self.division,
            '//': self.division,
            '^': self.exponentation,
            "multi_calculation": self.calculation_with_operators
        }
        self.result = 0
        self.variables = defaultdict(int)
        self.message_assignment = 'Invalid assignment'
        self.message_identifier = 'Invalid identifier'
        self.message_variable = 'Unknown variable'
        self.error_catching = None

    def addition(self, *args) -> int:
        additions = 0
        try:
            for number in args:
                if isinstance(number, list) and number:
                    for n in number:
                        additions += int(n)
                else:
                    additions += int(number)
            self.result += additions
            return additions
        except TypeError:
            pass

    def subtraction(self, *args) -> int:
        abstractions = 0
        try:
            for number in args:
                if isinstance(number, list) and number:
                    for n in number:
                        if abstractions == 0:
                            abstractions = int(n)
                        else:
                            abstractions -= int(n)
                else:
                    if abstractions == 0:
                        abstractions = int(number)
                    else:
                        abstractions -= int(number)
            self.result -= abstractions
            return abstractions
        except TypeError:
            pass

    def multiplication(self, *args) -> int:
        multiplications = 0
        try:
            for number in args:
                if isinstance(number, list) and number:
                    for n in number:
                        if multiplications == 0:
                            multiplications = int(n)
                        else:
                            multiplications *= int(n)
                else:
                    if multiplications == 0:
                        multiplications = int(number)
                    else:
                        multiplications *= int(number)
            self.result *= multiplications
            return multiplications
        except TypeError:
            pass

    def division(self, *args) -> int:
        division = 0
        try:
            for number in args:
                if isinstance(number, list) and number:
                    for n in number:
                        if division == 0:
                            division = int(n)
                        else:
                            try:
                                division /= int(n)
                            except ZeroDivisionError:
                                self.error_catching= "Division with zero impossible"
                                return False
                else:
                    if division == 0:
                        division = int(number)
                    else:
                        try:
                            division /= int(number)
                        except ZeroDivisionError:
                            self.error_catching = "Division with zero impossible"
                            return False
            self.result //= division
            return int(division)
        except TypeError:
            pass

    def exponentation(self, *args) -> int:
        exponent = 0
        try:
            for number in args:
                if isinstance(number, list) and number:
                    for n in number:
                        if exponent == 0:
                            exponent = int(n)
                        else:
                            exponent **= int(n)
                else:
                    if exponent == 0:
                        exponent = int(number)
                    else:
                        exponent **= int(number)
            self.result **= exponent
            return exponent
        except TypeError:
            pass

    def calculation_with_operators(self, *args):
        results = 0
        operation_to_do = None
        operators = {'+', '-', '*', '/', '^'}
        position = 0
        for number in args:
            if isinstance(number, list) and number:
                for j in number:
                    if str(j).isalpha():
                        if self.variable_validator(j):
                            j = self.variables[j]
                        else:
                            return self.error_catching
                    elif str(j).isnumeric():
                        j = int(j)
                    if operation_to_do is None and position == 0:
                        results = j
                        position += 1
                        continue
                    if j in operators:
                        operation_to_do = j
                        continue
                    results = self._calculations[operation_to_do](results, j)
                    operation_to_do = None
                    if results or results == 0:
                        continue
                    else:
                        return self.error_catching
        return results

    def variable_validator(self, *args):
        template_identifier = r'^ *[A-z]+ *='
        template_assignment_variable = r'^ ?[A-z]+$'
        template_assignment_value = r'^ ?[0-9]+$'
        template_variable_call = r'^ ?[A-z]+$'

        for arg in args:
            arg = arg.strip()
            if isinstance(arg, str):
                if re.match(template_identifier, arg):
                    cleaned_variable = re.sub(" ", "", arg).split("=")
                    if len(cleaned_variable) > 2:
                        self.error_catching = self.message_assignment
                        return False
                    variable, assignment = cleaned_variable
                    if re.match(template_assignment_variable, assignment):
                        if assignment in self.variables.keys():
                            self.variables[variable] = self.variables[assignment]
                            return True
                        else:
                            self.error_catching = self.message_variable
                            return False
                    if re.match(template_assignment_value, assignment):
                        self.variables[variable] = int(assignment)
                        return True
                    else:
                        self.error_catching = self.message_assignment
                        return False
                if re.match(template_variable_call, arg):
                    if self.variables.get(arg) is not None:
                        return True
                    else:
                        self.error_catching = self.message_variable
                        return False
                if arg.isnumeric():
                    return True
                self.error_catching = self.message_identifier
                return False

    def to_post_fix(self, *args):
        operators = {'+', '-', '*', '/', '(', ')', '^'}
        priority = {'+': 1, '-': 1, '*': 2, '/': 2, "//": 2, '^': 3}
        stack = []
        result = []

        for string in args:
            if isinstance(string, str):
                string = re.sub(" ", "", string)
                temporary_number = ''
                for number in string:
                    if number.isnumeric():
                        temporary_number += number
                        continue
                    if number.isalpha():
                        if self.variable_validator(number):
                            result.append(self.variables[number])
                        else:
                            print(self.error_catching)
                            return False
                        continue
                    else:
                        if temporary_number:
                            result.append(int(temporary_number))
                            temporary_number = ''
                        if number == "(":
                            stack.append(number)

                        elif number == ")":
                            oper = stack.pop()
                            while oper != "(":
                                result.append(oper)
                                oper = stack.pop()
                        else:
                            if number in operators:
                                try:

                                    while stack and priority[number] <= priority[stack[-1]]:
                                        result.append(stack.pop())
                                    stack.append(number)
                                except KeyError:
                                    stack.append(number)
                if temporary_number:
                    result.append(int(temporary_number))

        while stack:
            result.append(stack.pop())

        if "(" in result or ")" in result:
            print("Invalid expression")
            return False
        return result

    def calculate_post_fix(self, post_fix_result: list):
        stack = []
        operators = {'+', '-', '*', '/', '^'}
        for i in post_fix_result:
            if i not in operators:
                stack.append(i)
            else:
                if len(stack) > 1:
                    value_1 = stack.pop()
                    value_2 = stack.pop()
                    if value_2 is None:
                        value_2 = 0
                    calculation = [value_2, i, value_1]
                    result = self.calculation_with_operators(calculation)
                    stack.append(result)
        return stack[0]


    def remove_redundant_operators(self, *args: str):
        template_m_d_exp = r"(\*|/|\^){2,}"
        template_add = r"\+{2,}"
        template_minus_even = r"(--)+"
        template_minus_odd = r"-(--)*"
        template_add_minus = r"(\+-|-\+){1,}"
        substituted = None
        parenthesis_counter = 0

        for arg in args:
            substituted = re.sub(" ","", arg)
            test_1 = re.search(template_m_d_exp, substituted)
            test_2 = re.search(template_add, substituted)
            test_3 = re.search(template_minus_even, substituted)
            test_4 = re.search(template_minus_odd, substituted)

            if test_1:
                print("Invalid expression")
                return False
            if test_2:
                substituted = re.sub(template_add, "+", substituted)
            if test_3:
                substituted = re.sub(template_minus_even, "+", substituted)
            if test_4:
                substituted = re.sub(template_minus_odd, "-", substituted)
                test_5 = re.search(template_add_minus, substituted)
                if test_5:
                    substituted = re.sub(template_add_minus, "+", substituted)
        if "(" in substituted or ")" in substituted:
            for i in substituted:
                if i == "(":
                    parenthesis_counter += 1
                elif i == ")":
                    parenthesis_counter -= 1
            if parenthesis_counter != 0:
                print("Invalid expression")
                return False
        return substituted

    def __str__(self):
        return str(self.result)


calc = Calculator()

while True:
    numbers = input()
    if numbers.startswith("/") and numbers not in {"/exit", "/help"}:
        print("Unknown command")
        continue
    if numbers == "/exit":
        print("Bye!")
        break
    if numbers == "/help":
        print("The program calculates the sum and sub of numbers. Use '+' and '-' separated with space")
        continue
    if numbers.split():
        if "=" in numbers or numbers.strip().isalnum():
            if calc.variable_validator(numbers):
                pass
            else:
                print(calc.error_catching)
                continue

        if "=" not in numbers:
            cleared_input = calc.remove_redundant_operators(numbers)
            if cleared_input or cleared_input is None:
                pass
            else:
                continue
            post_fix = calc.to_post_fix(cleared_input)
            print(calc.calculate_post_fix(post_fix))

    if not numbers:
        continue

