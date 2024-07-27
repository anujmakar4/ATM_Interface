import datetime
import time

class User:
    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = pin

class Account:
    def __init__(self, user, balance=0):
        self.user = user
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        time.sleep(10)
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return None  # Insufficient funds
        self.balance -= amount
        return self.balance

    def transfer(self, target_account, amount):
        if amount > self.balance:
            return False  # Insufficient funds
        self.balance -= amount
        target_account.balance += amount
        return True

class Transaction:
    def __init__(self):
        self.history = []

    def add_transaction(self, transaction_type, amount, balance):
        self.history.append({
            'type': transaction_type,
            'amount': amount,
            'balance': balance,
            'time': datetime.datetime.now()
        })

    def get_history(self):
        return self.history

class Bank:
    def __init__(self):
        self.users = {}
        self.accounts = {}
        self.transactions = {}

    def add_user(self, user_id, pin):
        user = User(user_id, pin)
        self.users[user_id] = user
        self.accounts[user_id] = Account(user)
        self.transactions[user_id] = Transaction()

    def authenticate(self, user_id, pin):
        user = self.users.get(user_id)
        if user and user.pin == pin:
            return user
        return None

class ATM:
    def __init__(self, bank):
        self.bank = bank
        self.current_user = None

    def start(self):
        user_id = input("Enter user ID: ")
        pin = input("Enter PIN: ")

        user = self.bank.authenticate(user_id, pin)
        if user:
            self.current_user = user
            self.main_menu()
        else:
            print("Authentication failed!")

    def main_menu(self):
        while True:
            print("\n1. Transactions History")
            print("2. Withdraw")
            print("3. Deposit")
            print("4. Transfer")
            print("5. Quit")

            choice = input("Enter choice: ")

            if choice == '1':
                self.show_transaction_history()
            elif choice == '2':
                self.withdraw()
            elif choice == '3':
                self.deposit()
            elif choice == '4':
                self.transfer()
            elif choice == '5':
                break
            else:
                print("Invalid choice!")

    def show_transaction_history(self):
        history = self.bank.transactions[self.current_user.user_id].get_history()
        if not history:
            print("No transactions found.")
        else:
            for transaction in history:
                print(f"{transaction['time']} - {transaction['type']} - Amount: {transaction['amount']} - Balance: {transaction['balance']}")

    def withdraw(self):
        amount = float(input("Enter amount to withdraw: "))
        account = self.bank.accounts[self.current_user.user_id]
        new_balance = account.withdraw(amount)
        if new_balance is not None:
            self.bank.transactions[self.current_user.user_id].add_transaction('Withdraw', amount, new_balance)
            print(f"Withdrawn {amount}. New balance: {new_balance}")
        else:
            print("Insufficient funds.")

    def deposit(self):
        amount = float(input("Enter amount to deposit: "))
        account = self.bank.accounts[self.current_user.user_id]
        new_balance = account.deposit(amount)
        self.bank.transactions[self.current_user.user_id].add_transaction('Deposit', amount, new_balance)
        print(f"Deposited {amount}. New balance: {new_balance}")

    def transfer(self):
        target_user_id = input("Enter target user ID: ")
        amount = float(input("Enter amount to transfer: "))
        target_account = self.bank.accounts.get(target_user_id)
        if target_account:
            account = self.bank.accounts[self.current_user.user_id]
            success = account.transfer(target_account, amount)
            if success:
                self.bank.transactions[self.current_user.user_id].add_transaction('Transfer Out', amount, account.balance)
                self.bank.transactions[target_user_id].add_transaction('Transfer In', amount, target_account.balance)
                print(f"Transferred {amount} to {target_user_id}. New balance: {account.balance}")
            else:
                print("Insufficient funds.")
        else:
            print("Target account not found.")

# Example usage:
bank = Bank()
time.sleep(5)
bank.add_user("softy", "9604")
bank.add_user("surya", "0611")

atm = ATM(bank)
atm.start()
