# Write your code here

import secrets
import random
import string
import sqlite3


class BankingSystem:
    def __init__(self):
        self.data_base = {}
        self.card_number = None
        self.card_pin = None
        self.balance = None
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
            self.conn.commit()
        except sqlite3.OperationalError:
            print('', end='')

    def create_account(self):
        self.card_number = self.generate_card_number()
        self.card_pin = str(random.randint(1000,4000))
        self.balance = 0
        print("Your card has been created")
        print("Your card number:")
        print(int(self.card_number))
        print("Your card PIN:")
        print(self.card_pin)
        print()
        self.cur.execute('INSERT INTO card (number, pin, balance) VALUES({0},{1},{2})'.format(self.card_number, self.card_pin, self.balance))
        self.conn.commit()

    def check_card_number(self, card_number):
        card_digits = []
        counter = 0
        sum_card_numbers = 0
        number_ = 0
        for s in range(len(card_number)-1):
            card_digits.append(int(card_number[s]))

        while counter < len(card_digits):
            card_digits[counter] *= 2
            if card_digits[counter] > 9:
                card_digits[counter] -= 9
            counter += 2

        while number_ < len(card_digits):
            sum_card_numbers += card_digits[number_]
            number_ += 1

        if(sum_card_numbers + int(card_number[-1])) % 10 != 0:
            return [False, False]
        self.cur.execute('SELECT * FROM card WHERE number = {}'.format(card_number))
        query = self.cur.fetchone()
        if query is None:
            return [True, False]
        else:
            return [True, True]

    def log_into_account(self):

        print("Enter your card number:")
        c = int(input())
        print("Enter your PIN:")
        b = input()
        id = None
        number_ = None
        pin = None
        balance = None
        if self.check_card_number(str(c))[0] == False:
            print("Wrong card number or PIN!")
            menu1()
        try:
            self.cur.execute("SELECT * FROM card WHERE number = {}".format(str(c)))
            query = self.cur.fetchone()
            if query == None:
                print("Wrong card number or PIN!")
                menu1()
            else:
                id, number, pin, balance = query
                print(number_)

        except sqlite3.Error:
            print("Wrong card number or PIN!")
            menu1()
        try:
            if pin == b:
                print("You have successfully logged in!")
                print(query[1])
                self.successful_logon(query[1])
            else:
                print("Wrong card number or PIN!")
                menu1()
        except KeyError or TypeError:
            print("Wrong card number or PIN!")
            menu1()

    def successful_logon(self, number):
        number_ = number
        balance = None
        menu2()
        user_input2 = None
        query = None  # will be initialised when checked for balance in check balance
        while True:
            try:
                user_input2 = int(input())
            except ValueError:
                print('Enter Valid input')
            if user_input2 == 1:
                print('Balance will be shown')
                self.cur.execute('SELECT * FROM card WHERE number = {}'.format(number))
                query = self.cur.fetchone()
                print(end='')
                balance = query[-1]
                print("Balance: " + str(balance))
                menu2()
            elif user_input2 == 2:
                self.add_income(number)
                main()
            elif user_input2 == 3:
                self.do_transfer(number)
                main()
            elif user_input2 == 4:
                self.close_account(number)
                main()
            elif user_input2 == 5:
                print("You have successfully logged out!")
                main()
            elif user_input2 == 0:
                print("Bye!")
                exit()
            else:
                print("Select valid option")
                continue
    def add_income(self, number):  # check completed

        income_to_be_added = None
        print('Enter income:')
        self.cur.execute('SELECT * FROM card WHERE number = {}'.format(number))
        query = self.cur.fetchone()
        #  print(query)
        #  print('Executed here')
        #  print(query[1])
        income_to_be_added = int(input()) + query[3]
        self.cur.execute("UPDATE card SET balance = {0} WHERE number = {1}".format(income_to_be_added, number))
        self.conn.commit()
        print('Income was added!')
        self.successful_logon(query[1])

    def do_transfer(self, number):  # check completed
        print('Transfer')
        print('Enter card number:')
        to_cardnumber = input()
        if not self.check_card_number(to_cardnumber)[0]:
            print('Probably you made a mistake in the card number. Please try again!')  # if wrong card number then go back
            self.successful_logon(number)

        if not self.check_card_number(to_cardnumber)[1]:
            print('Such a card does not exist.')  # if the card number is as per the standard but it doesn't exist in database
            self.successful_logon(number)

        print('Enter how much money you want to transfer:')
        amount_to_be_transferred = int(input())
        self.cur.execute('SELECT * FROM card WHERE number = {}'.format(number))
        query = self.cur.fetchone()
        if query[3] < amount_to_be_transferred: # if account has low balance, program won't go further
            print('Not enough money!')
            self.successful_logon(number)

        self.cur.execute('SELECT * FROM card WHERE number = {}'.format(to_cardnumber))
        query2 = self.cur.fetchone()
        income_to_be_added = amount_to_be_transferred + query2[3]
        income_to_deducted = query[3] - amount_to_be_transferred
        self.cur.execute("UPDATE card SET balance = {0} WHERE number = {1}".format(income_to_be_added, to_cardnumber))
        self.cur.execute("UPDATE card SET balance = {0} WHERE number = {1}".format(income_to_deducted, number))
        self.conn.commit()
        print('Success!')
        self.successful_logon(number)

    def close_account(self, number):  # check completed
        self.cur.execute("DELETE FROM card WHERE number = {0}".format(number))
        self.conn.commit()
        print('The account has been closed!')
        main()

    def generate_card_number(self):
        a = str(400000)+str(''.join(secrets.choice(string.digits) for x in range(9)))
        card_digits = []
        counter = 0
        sum_card_numbers = 0
        last_digit = 0

        while counter < len(a):
            card_digits.append(int(a[counter]))
            counter += 1
        counter = 0

        while counter < len(card_digits):
            card_digits[counter] *= 2
            if card_digits[counter] > 9:
                card_digits[counter] -= 9
            counter += 2
        for i in range(len(card_digits)):
            sum_card_numbers += card_digits[i]

        if sum_card_numbers % 10 != 0:
            last_digit = 10 - sum_card_numbers % 10
        return a+str(last_digit)

    def data_view(self):
        #  print(self.data_base)
        try:
            self.cur.execute('SELECT * FROM card')
            print(self.cur.fetchall())
        except sqlite3.OperationalError:
            self.cur.execute('CREATE TABLE card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
            self.conn.commit()
            menu1()

    def drop_table(self):
        self.cur.execute('DROP TABLE card')
        self.conn.commit()
        print('dropped')

    def view_table_schema(self):
        self.cur.execute("pragma table_info('card')")
        print(self.cur.fetchall())

def main():
    menu1()
    user_input = None
    while True:
        try:
            user_input = int(input())
        except ValueError:
            print('Enter Valid input')

        if user_input == 1:
            a.create_account()
            menu1()
        elif user_input == 2:
            a.log_into_account()
        elif user_input == 0:
            print("Bye!")
            exit()
        elif user_input == 3:
            a.generate_card_number()
        elif user_input == 4:
            a.data_view()
        elif user_input == 5:
            a.drop_table()
        elif user_input == 6:
            a.view_table_schema()
        else:
            print("Select valid option")
            continue


def menu1():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    print()

def menu2():
        print()
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")


a = BankingSystem()
main()




