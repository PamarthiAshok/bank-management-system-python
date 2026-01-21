import sqlite3
connect = sqlite3.connect("Bank.db")
from functions import account_creation,pin_generation,balance_enquiry,deposit,withdrawal,account_transfer,change_pin
cursor = connect.cursor()


#SQL query for db
'''
cursor.execute("""
CREATE TABLE IF NOT EXISTS Accounts (
    account_number INTEGER PRIMARY KEY,
    account_holder_name TEXT NOT NULL,
    mobile TEXT UNIQUE,
    date_of_birth TEXT,
    address TEXT NOT NULL,
    email TEXT UNIQUE,
    aadhar TEXT UNIQUE,
    gender TEXT,
    account_type TEXT NOT NULL,
    balance REAL DEFAULT 1000,
    pin INTEGER DEFAULT 0
)
""")
connect.commit()
connect.close()
'''

print("-" * 15, "WELCOME TO BHARAT NATIONAL BANK", "-" * 15)

while True:
    print("""
1) Account Creation
2) PIN Generation
3) Balance Enquiry
4) Deposit
5) Withdrawal
6) Account Transfer
7) PIN Change
8) Exit
""")

    option = input("Select an option: ")

    if option == "1":
        print("\n--- Account Creation ---")

        name = input("Enter Account Holder Name: ")
        mobile = input("Enter Mobile Number: ")
        dob = input("Enter Date of Birth (YYYY-MM-DD): ")
        gender = input("Enter Gender (Male/Female/Other): ")
        address = input("Enter Address: ")
        email = input("Enter Email ID: ")
        aadhar = input("Enter Aadhar Number: ")

        print("\nSelect Account Type")
        print("1. Savings Account")
        print("2. Current Account")
        print("3. Joint Account")

        acc_type_choice = input("Enter your choice: ")

        if acc_type_choice == "1":
            account_type = "Savings"
        elif acc_type_choice == "2":
            account_type = "Current"
        elif acc_type_choice == "3":
            account_type = "Joint"
        else:
            print("Invalid Account Type Selection")
            continue

        account_creation(
            name=name,
            mobile=mobile,
            dob=dob,
            gender=gender,
            address=address,
            email=email,
            aadhar=aadhar,
            account_type=account_type
        )

    elif option == "2":
        account_num = int(input("Enter your Account Number: "))
        mobile = input("Enter your Mobile Number: ")
        aadhar = input("Enter Aadhar Number: ")
        pin_generation(account_num, mobile, aadhar)


    elif option == "3":
        account_num=int(input("Enter your Account Number:"))
        pin=input("Enter your Pin:")
        balance_enquiry(account_num,pin)

    elif option == "4":
        account_num=int(input("Enter your Account Number:"))
        pin=input("Enter your PIN:")
        deposit(account_num,pin)

    elif option == "5":
        account_num=int(input("Enter your Account Number:"))
        pin=input("Enter your PIN:")
        withdrawal(account_num,pin)

    elif option == "6":
        account_num=int(input("Enter your Account Number:"))
        pin=input("Enter your PIN:")
        account_transfer(account_num,pin)
    elif option == "7":
        account_num = int(input("Enter your Account Number: "))
        old_pin = input("Enter your Current PIN: ")
        change_pin(account_num,old_pin)

    elif option == "8":
        print("\nThank you for choosing Bharat National Bank")
        print("Visit Again 🙏")
        break

    else:
        print("Invalid option. Please try again.")
