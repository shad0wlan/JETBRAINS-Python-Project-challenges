from math import ceil
from math import log
import argparse
import sys

parser = argparse.ArgumentParser(description="This program is a loan calculator based on the parameters you provide")
parser.add_argument("--type")
parser.add_argument("--principal", type=int)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)
parser.add_argument("--payment", type=float)

args = parser.parse_args()


def check_for_negatives(*arguments):
    for i in arguments:
        if i is not None:
            if i < 0:
                print("Incorrect parameters")
                return False
    return True


def argument_validator(arguments):
    if len(sys.argv) != 5:
        print("Incorrect parameters")
        return False
    if arguments.type not in {"annuity", "diff"}:
        print("Incorrect parameters")
        return False
    if arguments.payment is not None and arguments.type == "diff":
        print("Incorrect parameters")
        return False
    if arguments.interest is None:
        print("Incorrect parameters")
        return False
    check_for_negatives(arguments.payment, arguments.interest, arguments.principal, arguments.periods)
    return True

def month_calculator_no_interest(loan, money_per_month):
    amount_of_months = ceil(loan / money_per_month)
    return amount_of_months


def monthly_payment_no_interest(loan, amount_of_months):
    amount = month_calculator_no_interest(loan, amount_of_months)
    last_payment = loan - (amount_of_months - 1) * amount
    if amount != last_payment:
        return amount, last_payment
    return amount


def total_repay_time(principal, annuity, loan_interest):
    i = loan_interest / (12 * 100)
    n = log((annuity / (annuity - i * principal)), 1 + i)
    return round(n)


def annuity_monthly_payment(principal, n, loan_interest):
    i = loan_interest / (12 * 100)
    payment = principal * (i * (1 + i) ** n) / ((1 + i) ** n - 1)
    return ceil(payment)


def principal_calculator(annuity, n, loan_interest):
    i = loan_interest / (12 * 100)
    principal = annuity / ((i * (1 + i) ** n) / ((1 + i) ** n - 1))
    return round(principal)


def differentiated_payment(principal, periods, loan_interest):
    i = loan_interest / (12 * 100)
    m = 1
    over = 0
    while m <= periods:
        d = principal // periods + i * (principal - (principal * (m - 1) // periods))
        print(f'Month {m}: payment is {ceil(d)}')
        over += ceil(d)
        m += 1
    return over

def user_action_annuity(arguments):

    loan_type = arguments.type
    loan_principal = arguments.principal
    loan_interest = arguments.interest
    loan_periods = arguments.periods
    loan_payment = arguments.payment
    if loan_type == "annuity":
        if loan_periods is None:
            loan_periods = total_repay_time(loan_principal, loan_payment, loan_interest)
            years = loan_periods // 12
            months = (loan_periods % 12) + 1
            years_str = "years" if years > 1 else "year"
            months_str = "months" if months > 1 else "month"
            if loan_periods > 12:
                if years == 0:
                    print(f'It will take {months} {months_str} to repay this loan!')
                elif months == 0:
                    print(f'It will take {years} {years_str} to repay this loan!')
                else:
                    print(f'It will take {years} {years_str} and {months} {months_str} to repay this loan!')
            else:
                print(f'It will take {months} {months_str} to repay this loan!')
            print()
        elif loan_principal is None:
            loan_principal = principal_calculator(loan_payment, loan_periods, loan_interest)
            print(f'Your loan principal = {loan_principal}!')

        else:
            loan_payment = annuity_monthly_payment(loan_principal, loan_periods, loan_interest)
            print(f'Your monthly payment = {loan_payment}!')
        overpayment = (loan_payment * loan_periods) - loan_principal
    else:
        loan_payment = differentiated_payment(loan_principal, loan_periods, loan_interest)
        overpayment = loan_payment - loan_principal
        print()

    print(f'Overpayment = {overpayment}')


def main():
    if argument_validator(args):
        user_action_annuity(args)


if __name__ == '__main__':
    main()