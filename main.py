# this is a sample project that was made to practice integrating json files into python
# and to practice nested dictionary stuff
# the code is a mess, sorry [not really]

import random
import time
import json
import sys

filename = 'accounts.json'
accounts_dict = {}


# import json file in write mode
def load_accounts(filename_var):
    try:
        with open(filename_var, 'r') as file:
            data = json.load(file)
            accounts_dict.update(data)
        return data
    except FileNotFoundError:
        return {}


# save function that uses json.dump to write new objects
def save_accounts(filename_input):
    with open(filename_input, 'w') as file:
        json.dump(accounts_dict, file, indent=2)


# assign a variable to the writeable dictionary
accounts = load_accounts(filename)


# main account generation function
def account_generator(fl_name):

    # create a unqiue, random 7-digit account number
    def generate_random_account_number():
        while True:
            random_n = int(random.randint(1000000, 9999999))
            if random_n not in accounts:
                return random_n

    # writes the randomly selected number to a variable, passes the acc# into a new dictionary
    # assign the acc# as a str, so it can be queried as a dict key in the json object
    def create_account(customer_name, initial_balance=0.0):

        account_number = generate_random_account_number()
        account_number = str(account_number)
        accounts_dict[account_number] = {
            'customer_name': customer_name,
            'balance': initial_balance,
            'transactions': []
        }
        return account_number

    # user information intake for account details
    def user_input():

        while True:
            customer_first = input("FIRST NAME: ").title().strip()
            if customer_first.isalpha():
                break
            else:
                print("[---INVALID FIRST NAME---]")

        while True:
            customer_last = input("LAST NAME: ").title().strip()
            if customer_last.isalpha():
                break
            else:
                print("[---INVALID LAST NAME---]")
        while True:
            try:
                initial_balance = float(input("INITIAL DEPOSIT: $"))
                break
            except ValueError:
                print("INVALID AMOUNT. IF NONE, TYPE '0.00'\n")

        # call the create_account function, badly hardcoded space between first and last name
        account_number = create_account(f"{customer_first}" " " f"{customer_last}", initial_balance)

        # save the account to the json file
        save_accounts(filename)

        print(f"\nNEW ACCOUNT: {account_number}")
        print(f"NAME: {accounts_dict.get(account_number, {}).get('customer_name')}")
        print(f"BALANCE: {accounts_dict.get(account_number, {}).get('balance')}")

    user_input()


# the main withdrawal/deposit function
def user_option():

    # withdrawal function
    def update_balance_with(acc_num, trans_num):
        if acc_num in accounts_dict:  # checks if acc# is in dictionary
            current_balance = accounts_dict[acc_num]['balance']  # assigns the balance value to a variable
            updated_balance = round(current_balance - trans_num, 2)  # assigns updated withdrawn balance to a variable
            accounts_dict[acc_num]['balance'] = updated_balance  # assigns updated balance to key value

            # record the transaction
            withdrawal_record = {
                'type': 'withdrawal',  # save interaction type
                'amount': trans_num,  # pass in transaction amount
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')  # pass in current time
            }

            # set transactions list to a var, using setdefault method
            transactions_list = accounts_dict.setdefault(acc_num, {}).setdefault('transactions', [])

            # set the max amount of dictionaries allowed in list to 2 + most recent, and assign to var
            transactions_list = [withdrawal_record] + transactions_list[:2]
            accounts_dict[acc_num]['transactions'] = transactions_list

            # accounts_dict.get(acc_num, {}).get('transactions').append(withdrawal_record)
            save_accounts(filename)  # saves the changes

    # depo function
    def update_balance_depo(acc_num, trans_num):
        if acc_num in accounts_dict:
            current_balance = accounts_dict[acc_num]['balance']
            updated_balance = round(current_balance + trans_num, 2)
            accounts_dict[acc_num]['balance'] = updated_balance

            deposit_record = {
                'type': 'deposit',
                'amount': trans_num,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }

            transactions_list = accounts_dict.setdefault(acc_num, {}).setdefault('transactions', [])

            transactions_list = [deposit_record] + transactions_list[:2]
            accounts_dict[acc_num]['transactions'] = transactions_list

            save_accounts(filename)

    inputacc = input("\nENTER ACCOUNT#: ").strip()
    # start a main loop for the deposit/withdrawal menu
    while True:
        try:
            # checks if acc# is in dict and prints acc details if found
            if str(inputacc) in accounts_dict:
                print(f"\nACCOUNT [{inputacc}]")

                # ran into many issues printing from a nested get, so i assinged it to a vairable first
                owner_name = accounts_dict.get(str(inputacc), {}).get('customer_name', 'N/A')

                # same here
                balance = accounts_dict.get(str(inputacc), {}).get('balance', 'N/A')
                print(f"OWNER: {owner_name}")
                print(f"AVAILABLE BALANCE: ${balance}")
                while True:  # new loop for the menu
                    try:  # passes input into menu with valueerror exception
                        with_depo = int(input("\n1. WITHDRAW\n2. DEPOSIT\n3. RETURN\n:: "))
                        if with_depo == 1:
                            with_amnt = float(input("\n[WITHDRAWAL MODE]\nENTER AMOUNT: $"))

                            # checks if enough $ is in acc

                            if with_amnt > accounts_dict.get(inputacc, {}).get('balance'):
                                print("\n[---INSUFFICIENT FUNDS---]")
                            else:

                                # subtracts user input from balance key value and assigns it to a var
                                update_balance_with(inputacc, with_amnt)  # calls update function and saves new values
                            break

                        elif with_depo == 2:

                            depo_amnt = float(input("\n[DEPOSIT MODE]\nENTER AMOUNT: $"))

                            update_balance_depo(inputacc, depo_amnt)  # calls depo function and saves new values
                            break
                        elif with_depo == 3:

                            print("\n")
                            return  # return to main menu
                    except ValueError:
                        print("\n[---INVALID INPUT---]")

            else:
                print("\n[---ACCOUNT NOT FOUND---]\n")
                break
        except ValueError:
            print("\n[---INVALID INPUT---]")


def information():
    while True:
        print("\n[this is an early python project\n")
        print("to learn how to integrate simple json objects\n")
        print("into a program that can dynamically edit them\n")
        print("also a start to interacting with nested dictionaries]\n")
        break


# main transaction function
def transactions_bundle():
    user_acc_tran = input("\nENTER ACCOUNT#: ")

    # make sure it's in the dict
    if user_acc_tran in accounts_dict:

        # start a for loop that cycles through transactions dictionaries
        for transaction in accounts_dict.get(user_acc_tran, {}).get('transactions', []):
            print(f"\nDATE: {transaction.get('timestamp')}\nTYPE: {transaction.get('type')}"f""
                  f"\nAMOUNT: {transaction.get('amount'):.2f}\n")
    else:
        print("\n[---INVALID ACCOUNT---]\n")


# main menu function, try:exception loop that calls all the functions
def main_menu():
    while True:
        try:
            while True:
                user_i = int(input("WELCOME TO BARD'S BAD BANK SIM\n\n1. CREATE NEW ACCOUNT\n"
                                   "2. WITHDRAW/DEPOSIT\n3. TRANSACTION HISTORY\n4. INFORMATION\n5. EXIT\n:: "))

                if user_i == 1:
                    account_generator('accounts.json')

                elif user_i == 2:
                    user_option()

                elif user_i == 3:
                    transactions_bundle()

                elif user_i == 4:
                    information()

                elif user_i == 5:
                    sys.exit("\nBARD'S BAD BANK SIM THANKS YOU FOR YOUR BUISNESS")

                else:
                    print("\n[---INVALID INPUT---]\n")
        except ValueError:
            print("\n[---INVALID INPUT---]\n")
            pass


main_menu()
