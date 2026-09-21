class BankAccount:
    def __init__(self, account_number, account_holder, balance):
        self.account_number = account_number
        self.account_holder = account_holder
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited {amount}. New balance: {self.__balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew {amount}. New balance: {self.__balance}")
        else:
            print("Insufficient funds or invalid withdrawal amount.")

    def get_balance(self):
        return self.__balance


print("Bank Account Details\n")
account_number = input("Enter the account number: ")
account_holder = input("Enter the account holder's name: ")
initial_balance = float(input("Enter the initial balance: "))
account = BankAccount(account_number, account_holder, initial_balance)
deposit_amount = float(input("Enter the amount to deposit: "))
account.deposit(deposit_amount)
withdraw_amount = float(input("Enter the amount to withdraw: "))
account.withdraw(withdraw_amount)
print(f"Final balance: {account.get_balance()}")

