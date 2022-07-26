# write your code here
from random import randrange


class Exam:
    maximum_mark = 5
    ar_operators = ["+", "-", "*"]

    def __init__(self):
        self.exam_answer = None
        self.exam_result = None
        self.difficulty = None
        self.exam_mark = 0

    def arithmetic_operation(self, operation_to_process):
        if self.difficulty == "1":
            first_value = operation_to_process[0]
            second_value = operation_to_process[2]
            if operation_to_process[1] == "+":
                return first_value + second_value
            elif operation_to_process[1] == "-":
                return first_value - second_value
            elif operation_to_process[1] == "*":
                return first_value * second_value
        elif self.difficulty == "2":
            return operation_to_process * operation_to_process


    def task_generator(self):
        if self.difficulty == "1":
            first_value = randrange(2, 10)
            second_value = randrange(2, 10)
            operation = self.ar_operators[randrange(len(self.ar_operators))]
            operation_to_process = [first_value, operation, second_value]
            result = self.arithmetic_operation(operation_to_process)
            self.exam_result = result
            print(*operation_to_process)
            return result, operation_to_process
        elif self.difficulty == "2":
            value_for_integral = randrange(11, 30)
            operation_to_process = value_for_integral
            result = self.arithmetic_operation(operation_to_process)
            self.exam_result = result
            print(operation_to_process)
            return result, operation_to_process

    def validate_exam_answer(self, user_input):

        try:
            exam_answer = int(user_input)
            if exam_answer == self.exam_result:
                print("Right!")
                self.exam_mark += 1
                return True

            else:
                print("Wrong!")
                return True
        except ValueError:
            print("Incorrect format.")
            self.take_exam_answer()

    def difficulty_validator(self):
        while True:
            difficulty = input("""Which level do you want? Enter a number:
1 - simple operations with numbers 2-9
2 - integral squares of 11-29
""")
            if difficulty not in {"1", "2"}:
                print("Incorrect format.")
            else:
                self.difficulty = difficulty
                return

    def take_exam_answer(self):
        self.exam_answer = input()
        self.validate_exam_answer(self.exam_answer)

    def take_exam(self):
        self.difficulty_validator()
        cnt = 0
        while cnt < self.maximum_mark:
            self.task_generator()
            self.take_exam_answer()
            cnt += 1
        print(f'Your mark is {self.exam_mark}/{self.maximum_mark}.')


class Candidate(Exam):

    def __init__(self, examination, name=None):
        self.name = name
        super().__init__()
        self.exam_mark = examination.exam_mark
        self.difficulty = examination.difficulty

    def set_student_name(self, name):
        self.name = name

    def difficulty_info(self):
        if self.difficulty == "1":
            return 'level 1 (simple operations with numbers 2-9).'
        elif self.difficulty == "2":
            return 'level 2 ( integral squares 11-29)'

    def save_results(self):
        answer = input("Would you like to save your result to the file? Enter yes or no.")

        if answer in {"yes", "YES", "y", "Yes"}:
            self.name = input("What is your name?\n")
            with open("results.txt", "a") as f:
                f.writelines(f'{self.name.capitalize()}: {self.exam_mark}/{self.maximum_mark} in {self.difficulty_info()}')
            print(f'The results are saved in "{f.name}".')
        else:
            return


test = Exam()
test.take_exam()
student = Candidate(test)
student.save_results()


