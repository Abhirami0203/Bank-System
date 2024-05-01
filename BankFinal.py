import mysql.connector
from datetime import datetime
from prettytable import PrettyTable

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abhi",
    database="bank"
)

class Bank:
    def __init__(self):
        self.cursor = mydb.cursor()

    def main(self):
        print("-" * 100)
        print("Welcome to Metro Bank".center(100))
        print("-" * 100)

    def customer_panel(self):
        print("-" * 100)
        print("Welcome to Customer Panel".center(100))
        print("-" * 100)
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. View Transaction History")
        print("5. View Profile")
        print("6. Exit")
        print("-" * 100)

    def staff_panel(self):
        print("-" * 100)
        print("Welcome to Staff Panel".center(100))
        print("-" * 100)
        print("1. Create Account")
        print("2. View Transaction History")
        print("3. View All Accounts")
        print("4. Remove an account")
        print("5. Edit/Update Customer Profile")
        print("6. Exit")
        print("-" * 100)

    def customer_login(self):
        print("-" * 100)
        print("Welcome to Customer login".center(100))
        print("-" * 100)

        while True:
            name = input("Enter your name: ")
            password = input("Enter your password: ")

            # Check if the entered name contains only alphabetic characters
            if not name.isalpha():
                print("Error: Name should contain only alphabetic characters.")
                continue

            # Check if the entered password is not empty
            if not password:
                print("Error: Password cannot be empty.")
                continue

            sql = "SELECT * FROM customer WHERE name = %s AND password = %s"
            val = (name, password)
            self.cursor.execute(sql, val)
            result = self.cursor.fetchone()

            if result:
                print("Customer login successful.")
                return name
            else:
                print("Invalid customer credentials... Please try again.")

    def staff_login(self):
        print("-" * 100)
        print("Welcome to staff login".center(100))
        print("-" * 100)
        staff_username = input("Enter staff username: ")
        staff_password = input("Enter staff password: ")
        sql = "SELECT * FROM staff WHERE staff_name = %s AND password = %s"
        val = (staff_username, staff_password)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()

        if result:
            print("Staff login successful.")
            return True
        else:
            print("Invalid staff credentials... Please try again.")
            return False

    def create_account(self):
        name = input("Enter account holder name: ")
        while True:
            if name.isalpha():
                break
            else:
                print("Invalid name. Name should contain only alphabetic characters.")
                name = input("Enter account holder name: ")

        # Prompt for phone number and validate
        while True:
            phone = input("Enter phone number (should not exceed 10 digits): ")
            if phone.isdigit() and len(phone) == 10:
                break
            else:
                print("Invalid phone number. Please enter a valid phone number with at most 10 digits.")

        while True:
            email = input("Enter your email (format: abc@gmail.com): ")
            if '@' in email and '.' in email:
                break
            else:
                print("Invalid email format. Please enter a valid email address.")
        gender = input("Enter your gender: ")
        address = input("Enter your address: ")
      
        type = input("Enter the type of account [S/C]: ")

        while True:
            balance = int(input("Enter the Initial amount (>=500 for Saving and >=1000 for current): "))
            if balance >= 500 and type == 'S':
                break
            elif balance >= 1000 and type == 'C':
                break
            else:
                print("Initial balance should be at least 500 for Savings and 1000 for Current accounts.")

        password = input("Enter the password: ")

        sql1 = "INSERT INTO accounts(name, email, phone_number, gender, address, balance, type) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val1 = (name, email, phone, gender, address, balance, type)
        self.cursor.execute(sql1, val1)
        mydb.commit()

        account_no = self.cursor.lastrowid

        # Inserting data into the customer table with the account number
        sql2 = "INSERT INTO customer(name, password, account_no) VALUES (%s, %s, %s)"
        val2 = (name, password, account_no)
        self.cursor.execute(sql2, val2)
        mydb.commit()
        # Insert initial deposit transaction into transactions table
        transaction_type = "deposit"
        timestamp = datetime.now()
        sql3 = "INSERT INTO transactions(account_no, transaction_type, amount, timestamp) VALUES (%s, %s, %s, %s)"
        val3 = (account_no, transaction_type, balance, timestamp)
        self.cursor.execute(sql3, val3)
        mydb.commit()
        print(f"Hello {name}, your account has been created successfully.")
        print(f"Account Number: {account_no}, Initial balance: {balance}")

    def view_profile(self, account_no):
        sql = "SELECT * FROM accounts WHERE account_no = %s"
        val = (account_no,)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()
        if result:
            print("Profile Information")
            print()
            print(f"Name: {result[1]}")
            print(f"Email: {result[2]}")
            print(f"Phone Number: {result[3]}")
            print(f"Gender: {result[4]}")
            print(f"Address: {result[5]}")
            print(f"Balance: {result[6]}")
            print(f"Account Type: {result[7]}")
        else:
            print("Profile not found for the given account number.")

    def delete_account(self, account_no):
        # Delete customer record
        sql_delete_customer = "DELETE FROM customer WHERE account_no = %s"
        val_delete_customer = (account_no,)
        self.cursor.execute(sql_delete_customer, val_delete_customer)
        mydb.commit()

        # Delete transactions related to the account
        sql_delete_transactions = "DELETE FROM transactions WHERE account_no = %s"
        val_delete_transactions = (account_no,)
        self.cursor.execute(sql_delete_transactions, val_delete_transactions)
        mydb.commit()

        # Fetch account details before deletion
        sql_fetch_account = "SELECT * FROM accounts WHERE account_no = %s"
        val_fetch_account = (account_no,)
        self.cursor.execute(sql_fetch_account, val_fetch_account)
        account_details = self.cursor.fetchone()

        if account_details:
            account_holder_name = account_details[1]  # Assuming account holder name is stored in the second column
            email = account_details[2]  # Assuming email is stored in the third column

            # Display account details before deletion
            print("Deleting account for:", account_holder_name)
            print("Account Details:")
            print("Account Number:", account_no)
            print("Account Holder Name:", account_holder_name)
            print("Email:", email)

            # Perform account deletion
            sql_delete_account = "DELETE FROM accounts WHERE account_no = %s"
            val_delete_account = (account_no,)
            self.cursor.execute(sql_delete_account, val_delete_account)
            mydb.commit()

            print("Account deleted successfully.")
        else:
            print("No account found with the given account number.")

    def deposit(self, amount):
        account_no = input("Enter the account number: ")

        previous_balance = self.get_balance(account_no)

        sql = "UPDATE accounts SET balance = balance + %s WHERE account_no = %s"
        val = (amount, account_no)
        self.cursor.execute(sql, val)
        mydb.commit()

        new_balance = self.get_balance(account_no)

        print(f"Deposit successful. Previous balance: {previous_balance}, Current balance: {new_balance}")

        transaction_type = "deposit"
        timestamp = datetime.now()
        sql = "INSERT INTO transactions(account_no, transaction_type, amount, timestamp) VALUES (%s, %s, %s, %s)"
        val = (account_no, transaction_type, amount, timestamp)
        self.cursor.execute(sql, val)
        mydb.commit()

    def withdraw(self, amount):     
        account_no = input("Enter the account number: ")
        account_type = self.get_account_type(account_no)
        minimum_balance = 500 if account_type == "S" else 1000

        current_balance = self.get_balance(account_no)

        if current_balance is None:
            print("Invalid account number.")
            return

        if current_balance - amount < minimum_balance:
            print(
                f"Error: Insufficient balance. Minimum balance for {account_type} account is {minimum_balance}."
            )
            return

        if current_balance < amount:
            print("Error: Insufficient balance.")
            return
        
        previous_balance = current_balance

        sql = "UPDATE accounts SET balance = balance - %s WHERE account_no = %s"
        val = (amount, account_no)
        self.cursor.execute(sql, val)
        mydb.commit()

        new_balance = self.get_balance(account_no)
        print(
            f"Withdrawal successful. Previous balance: {current_balance}, Current balance: {new_balance}"
        )

        transaction_type = "withdrawal"
        timestamp = datetime.now()
        sql = "INSERT INTO transactions(account_no, transaction_type, amount, timestamp) VALUES (%s, %s, %s, %s)"
        val = (account_no, transaction_type, amount, timestamp)
        self.cursor.execute(sql, val)
        mydb.commit()

    def get_balance(self, account_no):
        sql = "SELECT balance FROM accounts WHERE account_no = %s"
        val = (account_no,)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()
        return result[0] if result else None

    def check_balance(self):
        account_no = input("Enter the account number: ")
        balance = self.get_balance(account_no)
        if balance is not None:
            print(f"Account Balance: {balance}")
        else:
            print("Invalid account number.")

    def get_account_type(self, account_no):
        sql = "SELECT type FROM accounts WHERE account_no = %s"
        val = (account_no,)
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()
        return result[0] if result else None

    def view_customer_transaction_history(self, customer_name=None, account_no=None):
        if not customer_name and not account_no:
            print("Please provide either customer name or account number.")
            return

        if customer_name:
            # Get account number of the customer
            sql_get_account = "SELECT account_no FROM customer WHERE name = %s"
            val_get_account = (customer_name,)
            self.cursor.execute(sql_get_account, val_get_account)
            account_no_result = self.cursor.fetchone()

            if account_no_result:
                account_no = account_no_result[0]
            else:
                print(f"No account found for customer: {customer_name}")
                return

        if account_no:
            sql = """
            SELECT 
                c.name AS Customer_Name,
                a.email AS Customer_Email,
                a.address AS Customer_Address,
                t.transaction_id,
                t.transaction_type,
                t.amount,
                DATE_FORMAT(t.timestamp, '%Y-%m-%d') AS transaction_date,
                DATE_FORMAT(t.timestamp, '%H:%i:%s') AS transaction_time
            FROM 
                transactions t
            INNER JOIN accounts a ON t.account_no = a.account_no
            INNER JOIN customer c ON a.account_no = c.account_no
            WHERE 
                t.account_no = %s
            ORDER BY c.name, t.timestamp
            """
            val = (account_no,)
            self.cursor.execute(sql, val)
        else:
            sql = """
            SELECT 
                c.name AS Customer_Name,
                a.email AS Customer_Email,
                a.address AS Customer_Address,
                t.transaction_id,
                t.transaction_type,
                t.amount,
                DATE_FORMAT(t.timestamp, '%Y-%m-%d') AS transaction_date,
                DATE_FORMAT(t.timestamp, '%H:%i:%s') AS transaction_time
            FROM 
                transactions t
            INNER JOIN accounts a ON t.account_no = a.account_no
            INNER JOIN customer c ON a.account_no = c.account_no
            ORDER BY c.name, t.timestamp
            """
            self.cursor.execute(sql)

        transactions = self.cursor.fetchall()

        if transactions:
            current_customer = None

            for transaction in transactions:
                customer_name = transaction[0]

                if customer_name != current_customer:
                    if current_customer is not None:
                        print(table)  # Print the table before starting a new customer
                        print()  # Add empty line between tables
                    # Print customer information
                    print(f"Customer Name: {transaction[0]}")
                    print(f"Customer Email: {transaction[1]}")
                    print(f"Customer Address: {transaction[2]}")
                    # Create a new table for the transaction history of the current customer
                    table = PrettyTable(
                        ["Transaction ID", "Transaction Type", "Amount", "Date", "Time"]
                    )
                    current_customer = customer_name

                # Add transaction data to the table
                table.add_row(transaction[3:])

            # Print the last table after the loop completes
            print(table)
        else:
            print("No transactions found.")



    def view_transaction_history(self, account_no=None):
        if account_no:
            sql = """
            SELECT 
                c.name AS Customer_Name,
                a.email AS Customer_Email,
                a.address AS Customer_Address,
                t.transaction_id,
                t.transaction_type,
                t.amount,
                DATE_FORMAT(t.timestamp, '%Y-%m-%d') AS transaction_date,
                DATE_FORMAT(t.timestamp, '%H:%i:%s') AS transaction_time
            FROM 
                transactions t
            INNER JOIN accounts a ON t.account_no = a.account_no
            INNER JOIN customer c ON a.account_no = c.account_no
            WHERE 
                t.account_no = %s
            ORDER BY c.name, t.timestamp
            """
            val = (account_no,)
            self.cursor.execute(sql, val)
        else:
            sql = """
            SELECT 
                c.name AS Customer_Name,
                a.email AS Customer_Email,
                a.address AS Customer_Address,
                t.transaction_id,
                t.transaction_type,
                t.amount,
                DATE_FORMAT(t.timestamp, '%Y-%m-%d') AS transaction_date,
                DATE_FORMAT(t.timestamp, '%H:%i:%s') AS transaction_time
            FROM 
                transactions t
            INNER JOIN accounts a ON t.account_no = a.account_no
            INNER JOIN customer c ON a.account_no = c.account_no
            ORDER BY c.name, t.timestamp
            """
            self.cursor.execute(sql)
  
        transactions = self.cursor.fetchall()

        if transactions:
            current_customer = None

            for transaction in transactions:
                customer_name = transaction[0]

                if customer_name != current_customer:
                    if current_customer is not None:
                        print(table)  # Print the table before starting a new customer  # noqa: F821
                        print()  # Add empty line between tables
                    # Print customer information
                    print(f"Customer Name: {transaction[0]}")
                    print(f"Customer Email: {transaction[1]}")
                    print(f"Customer Address: {transaction[2]}")
                    # Create a new table for the transaction history of the current customer
                    table = PrettyTable(
                        ["Transaction ID", "Transaction Type", "Amount", "Date", "Time"]
                    )
                    current_customer = customer_name

                # Add transaction data to the table
                table.add_row(transaction[3:])

            # Print the last table after the loop completes
            print(table)
        else:
            print("No transactions found.")

    def edit_customer_profile(self, account_no):
        print("-" * 100)
        print("Edit Customer Profile".center(100))
        print("-" * 100)

        # Fetch the current profile information
        sql_select = "SELECT * FROM accounts WHERE account_no = %s"
        val_select = (account_no,)
        self.cursor.execute(sql_select, val_select)
        current_profile = self.cursor.fetchone()

        if current_profile:
            print("Current Profile Information:")
            print(f"1. Name: {current_profile[1]}")
            print(f"2. Email: {current_profile[2]}")
            print(f"3. Phone Number: {current_profile[3]}")
            print(f"4. Gender: {current_profile[4]}")
            print(f"5. Address: {current_profile[5]}")
            print("-" * 100)

            field_choice = input("Enter the number of the field you want to modify: ")
            field_name = ""
            new_value = ""

            if field_choice == "1":
                field_name = "name"
                new_value = input("Enter updated name: ")
            elif field_choice == "2":
                field_name = "email"
                new_value = input("Enter updated email: ")
            elif field_choice == "3":
                field_name = "phone_number"
                new_value = input("Enter updated phone number: ")
            elif field_choice == "4":
                field_name = "gender"
                new_value = input("Enter updated gender: ")
            elif field_choice == "5":
                field_name = "address"
                new_value = input("Enter updated address: ")
            else:
                print("Invalid choice.")
                return

            # Update the profile in the database
            sql_update = f"UPDATE accounts SET {field_name} = %s WHERE account_no = %s"
            val_update = (new_value, account_no)
            self.cursor.execute(sql_update, val_update)
            mydb.commit()

            print("Customer profile updated successfully.")
        else:
            print("Profile not found for the given account number.")

print("-" * 100)
print("Welcome to Metro Bank".center(100))
print("-" * 100)
print("1. Customer Login\n2. Staff Login")
login_choice = input("Select login type: ")

if login_choice == "1":
    bank = Bank()
    customer_name = None
    if (customer_name := bank.customer_login()):
        while True:
            bank.customer_panel()
            choice = input("Select any option: ")
            if choice == "1":
                amount = int(input("Enter amount to deposit: "))
                bank.deposit(amount)
            elif choice == "2":
                amount = int(input("Enter amount to withdraw: "))
                bank.withdraw(amount)
            elif choice == "3":
                bank.check_balance()
            elif choice == "4":
                bank.view_customer_transaction_history(customer_name)
            elif choice == "5":
                bank.view_profile(customer_name)
            elif choice == "6":
                print("Exiting Customer Panel...")
                break
            else:
                print("Invalid choice. Please try again.")

elif login_choice == "2":
    bank = Bank()
    if bank.staff_login():
        while True:
            bank.staff_panel()
            choice = input("Select any option: ")
            if choice == "1":
                bank.create_account()
            elif choice == "2":
                bank.view_transaction_history()
            elif choice == "3":
                bank.view_transaction_history()
            elif choice == "4":
                account_no = input("Enter the account number to delete: ")
                bank.delete_account(account_no)
            elif choice == "5":
                bank.edit_customer_profile(account_no)
            elif choice == "6":
                print("Exiting Staff Panel...")
                break
            else:
                print("Invalid choice. Please try again.")

else:
    print("Invalid choice.")
