from decimal import Decimal

class BankAccount:
    def __init__(self, account_number, owner_name):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = Decimal('0.0')

    def deposit(self, amount):
        amount = Decimal(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        amount = Decimal(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        return self.balance

    def get_balance(self):
        return self.balance

class Transaction:
    def __init__(self, account, transaction_type, amount):
        self.account = account
        self.transaction_type = transaction_type
        self.amount = Decimal(amount)
        self.balance_after_transaction = self.process_transaction()

    def process_transaction(self):
        if self.transaction_type == 'deposit':
            return self.account.deposit(self.amount)
        elif self.transaction_type == 'withdraw':
            return self.account.withdraw(self.amount)
        else:
            raise ValueError("Invalid transaction type.")

class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, owner_name):
        if account_number in self.accounts:
            raise ValueError("Account number already exists.")
        new_account = BankAccount(account_number, owner_name)
        self.accounts[account_number] = new_account
        return new_account

    def get_account(self, account_number):
        if account_number not in self.accounts:
            raise ValueError("Account does not exist.")
        return self.accounts[account_number]

# Demo usage
bank = Bank()
acc1 = bank.create_account('123', 'Alice')
acc2 = bank.create_account('456', 'Bob')

transaction1 = Transaction(acc1, 'deposit', '1000')
transaction2 = Transaction(acc2, 'deposit', '500')
transaction3 = Transaction(acc1, 'withdraw', '200')

print(f"Account 123 balance: {acc1.get_balance()}")
print(f"Account 456 balance: {acc2.get_balance()}")