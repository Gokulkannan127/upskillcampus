# BankingInformationSystem.py
# A simple Banking Information System for the Summer Internship Project

import json
import os
from datetime import datetime

class BankAccount:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transactions = []
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log initial transaction
        if initial_balance > 0:
            self._add_transaction("Deposit", initial_balance, "Initial deposit")
    
    def _add_transaction(self, transaction_type, amount, description=""):
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": transaction_type,
            "amount": amount,
            "balance_after": self.balance,
            "description": description
        }
        self.transactions.append(transaction)
    
    def deposit(self, amount):
        if amount <= 0:
            return {"status": "error", "message": "Deposit amount must be greater than 0"}
        
        self.balance += amount
        self._add_transaction("Deposit", amount, "Cash deposit")
        return {
            "status": "success",
            "message": f"Successfully deposited ₹{amount}",
            "new_balance": self.balance
        }
    
    def withdraw(self, amount):
        if amount <= 0:
            return {"status": "error", "message": "Withdrawal amount must be greater than 0"}
        
        if amount > self.balance:
            return {
                "status": "error",
                "message": "Insufficient balance",
                "available_balance": self.balance
            }
        
        self.balance -= amount
        self._add_transaction("Withdrawal", amount, "Cash withdrawal")
        return {
            "status": "success",
            "message": f"Successfully withdrew ₹{amount}",
            "new_balance": self.balance
        }
    
    def get_balance(self):
        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "balance": self.balance,
            "created_date": self.created_date
        }
    
    def get_transaction_history(self):
        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "transactions": self.transactions,
            "total_transactions": len(self.transactions)
        }
    
    def to_dict(self):
        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "balance": self.balance,
            "created_date": self.created_date,
            "transactions": self.transactions
        }

class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self.data_file = "bank_data.json"
        self.load_data()
    
    def load_data(self):
        """Load account data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    for account_data in data:
                        account = BankAccount(
                            account_data["account_number"],
                            account_data["account_holder"],
                            account_data["balance"]
                        )
                        account.created_date = account_data["created_date"]
                        account.transactions = account_data["transactions"]
                        self.accounts[account.account_number] = account
                print("Data loaded successfully!")
            except Exception as e:
                print(f"Error loading data: {e}")
        else:
            print("No existing data file found. Starting with empty system.")
    
    def save_data(self):
        """Save all account data to JSON file"""
        try:
            data = [account.to_dict() for account in self.accounts.values()]
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)
            print("Data saved successfully!")
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def create_account(self, account_holder, initial_balance=0):
        """Create a new bank account"""
        if not account_holder:
            return {"status": "error", "message": "Account holder name is required"}
        
        # Generate account number (simple sequential)
        if not self.accounts:
            account_number = "1001"
        else:
            max_num = max(int(acc_num) for acc_num in self.accounts.keys())
            account_number = str(max_num + 1)
        
        account = BankAccount(account_number, account_holder, initial_balance)
        self.accounts[account_number] = account
        self.save_data()
        
        return {
            "status": "success",
            "message": f"Account created successfully for {account_holder}",
            "account_number": account_number,
            "initial_balance": initial_balance
        }
    
    def get_account(self, account_number):
        """Get account by account number"""
        if account_number not in self.accounts:
            return {"status": "error", "message": "Account not found"}
        return {"status": "success", "account": self.accounts[account_number]}
    
    def deposit(self, account_number, amount):
        """Deposit money to an account"""
        if account_number not in self.accounts:
            return {"status": "error", "message": "Account not found"}
        
        result = self.accounts[account_number].deposit(amount)
        if result["status"] == "success":
            self.save_data()
        return result
    
    def withdraw(self, account_number, amount):
        """Withdraw money from an account"""
        if account_number not in self.accounts:
            return {"status": "error", "message": "Account not found"}
        
        result = self.accounts[account_number].withdraw(amount)
        if result["status"] == "success":
            self.save_data()
        return result
    
    def get_balance(self, account_number):
        """Get account balance"""
        if account_number not in self.accounts:
            return {"status": "error", "message": "Account not found"}
        return {"status": "success", "data": self.accounts[account_number].get_balance()}
    
    def get_transactions(self, account_number):
        """Get transaction history"""
        if account_number not in self.accounts:
            return {"status": "error", "message": "Account not found"}
        return {"status": "success", "data": self.accounts[account_number].get_transaction_history()}
    
    def get_all_accounts(self):
        """Get all account numbers"""
        return {"status": "success", "accounts": list(self.accounts.keys())}

def main():
    system = BankingSystem()
    
    while True:
        print("\n" + "="*50)
        print("🏦 BANKING INFORMATION SYSTEM")
        print("="*50)
        print("1. Create New Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. View Transaction History")
        print("6. View All Accounts")
        print("7. Save Data")
        print("8. Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            name = input("Enter account holder name: ").strip()
            try:
                balance = float(input("Enter initial deposit amount (0 for no deposit): ").strip())
                if balance < 0:
                    print("Initial balance cannot be negative!")
                    continue
            except ValueError:
                print("Invalid amount! Please enter a valid number.")
                continue
            
            result = system.create_account(name, balance)
            print(f"\n{result['message']}")
            if result['status'] == 'success':
                print(f"Account Number: {result['account_number']}")
                print(f"Initial Balance: ₹{result['initial_balance']}")
        
        elif choice == "2":
            acc_num = input("Enter account number: ").strip()
            try:
                amount = float(input("Enter amount to deposit: ").strip())
                if amount <= 0:
                    print("Amount must be greater than 0!")
                    continue
            except ValueError:
                print("Invalid amount! Please enter a valid number.")
                continue
            
            result = system.deposit(acc_num, amount)
            print(f"\n{result['message']}")
            if result['status'] == 'success':
                print(f"New Balance: ₹{result['new_balance']}")
        
        elif choice == "3":
            acc_num = input("Enter account number: ").strip()
            try:
                amount = float(input("Enter amount to withdraw: ").strip())
                if amount <= 0:
                    print("Amount must be greater than 0!")
                    continue
            except ValueError:
                print("Invalid amount! Please enter a valid number.")
                continue
            
            result = system.withdraw(acc_num, amount)
            print(f"\n{result['message']}")
            if result['status'] == 'success':
                print(f"New Balance: ₹{result['new_balance']}")
        
        elif choice == "4":
            acc_num = input("Enter account number: ").strip()
            result = system.get_balance(acc_num)
            
            if result['status'] == 'success':
                data = result['data']
                print("\n📊 ACCOUNT BALANCE")
                print("-"*30)
                print(f"Account Holder: {data['account_holder']}")
                print(f"Account Number: {data['account_number']}")
                print(f"Current Balance: ₹{data['balance']}")
                print(f"Account Created: {data['created_date']}")
            else:
                print(f"\n{result['message']}")
        
        elif choice == "5":
            acc_num = input("Enter account number: ").strip()
            result = system.get_transactions(acc_num)
            
            if result['status'] == 'success':
                data = result['data']
                print(f"\n📜 TRANSACTION HISTORY FOR {data['account_holder']}")
                print("="*60)
                print(f"Account Number: {data['account_number']}")
                print(f"Total Transactions: {data['total_transactions']}")
                print("-"*60)
                
                if not data['transactions']:
                    print("No transactions found.")
                else:
                    for idx, txn in enumerate(data['transactions'], 1):
                        print(f"{idx}. {txn['date']}")
                        print(f"   Type: {txn['type']} | Amount: ₹{txn['amount']}")
                        print(f"   Balance After: ₹{txn['balance_after']}")
                        print(f"   Description: {txn['description']}")
                        print("-"*60)
            else:
                print(f"\n{result['message']}")
        
        elif choice == "6":
            result = system.get_all_accounts()
            if result['status'] == 'success':
                accounts = result['accounts']
                print(f"\n📋 TOTAL ACCOUNTS: {len(accounts)}")
                print("-"*30)
                if accounts:
                    for acc_num in accounts:
                        acc = system.accounts[acc_num]
                        print(f"Account {acc_num}: {acc.account_holder} | Balance: ₹{acc.balance}")
                else:
                    print("No accounts available.")
        
        elif choice == "7":
            if system.save_data():
                print("Data saved to file successfully!")
            else:
                print("Failed to save data!")
        
        elif choice == "8":
            print("\nThank you for using the Banking Information System!")
            print("Saving data before exit...")
            system.save_data()
            break
        
        else:
            print("\nInvalid choice! Please select a valid option (1-8).")

if __name__ == "__main__":
    main()