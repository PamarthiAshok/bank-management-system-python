import sqlite3

# Database connection
connect = sqlite3.connect("Bank.db")
cursor = connect.cursor()


def get_next_account_number():
    """
    Returns the next account number.
    If no records exist, returns the default first account number.
    """
    DEFAULT_ACCOUNT_NUMBER = 202500000001  # 12-digit starting number

    cursor.execute("SELECT account_number FROM Accounts")
    records = cursor.fetchall()

    if not records:
        return DEFAULT_ACCOUNT_NUMBER

    account_numbers = [row[0] for row in records]
    return max(account_numbers) + 1



def account_creation(name, mobile, dob, gender, address, email, aadhar, account_type):
    #STEP 1: get auto-incremented account number
    account_number = get_next_account_number()

    #STEP 2: reuse the SAME account_number everywhere
    cursor.execute("""
        INSERT INTO Accounts (
            account_number,
            account_holder_name,
            mobile,
            date_of_birth,
            address,
            email,
            aadhar,
            gender,
            account_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        account_number,
        name,
        mobile,
        dob,
        address,
        email,
        aadhar,
        gender,
        account_type
    ))

    connect.commit()

    #STEP 3: reuse again for display
    print("\n Account Created Successfully")
    print(f"🏦 Your Account Number is: {account_number}")

def pin_generation(account_number, mobile, aadhar):
    cursor.execute(
        "SELECT mobile, aadhar FROM Accounts WHERE account_number = ?",
        (account_number,))
    record = cursor.fetchone()

    if not record:
        print("Invalid Account Number")
        return

    if mobile != record[0] or aadhar != record[1]:
        print("Verification Failed")
        return

    pin = input("Enter 4-digit PIN: ")
    confirm_pin = input("Confirm PIN: ")

    if pin != confirm_pin:
        print("PIN mismatch")
        return

    cursor.execute(
        "UPDATE Accounts SET pin = ? WHERE account_number = ?",
        (pin, account_number)
    )

    connect.commit()
    print("PIN Generated Successfully")

def balance_enquiry(account_num,pin):
    cursor.execute("SELECT pin,balance from Accounts where account_number=?",(account_num,))
    record=cursor.fetchone()
    if not record:
        print("Invalid Account Number")
        return
    sorted_pin,balance=record
    if str(pin)!=str(sorted_pin):
        print("Invalid PIN")
        return
    print(f"Your Current Balance is: ₹{balance}")


def deposit(account_num,pin):
    cursor.execute("SELECT pin,balance from Accounts where account_number=?",(account_num,))
    record=cursor.fetchone()
    if not record:
        print("Invalid Account Number")
        return
    sorted_pin,balance=record
    if str(pin)!=str(sorted_pin):
        print("Invalid PIN")
        return
    deposit_amount=float(input("Enter amount to deposit:"))
    if deposit_amount<=0:
        print("Deposit amount must be positive")
        return
    new_balance=balance+deposit_amount
    cursor.execute("UPDATE Accounts SET balance = ? where account_number=?",(new_balance,account_num))
    connect.commit()
    print("Deposit Successful")
    print("Updated Balance: ₹{new_balance}")


def withdrawal(account_num, pin):
    cursor.execute(
        "SELECT pin, balance FROM Accounts WHERE account_number = ?",
        (account_num,)
    )
    record = cursor.fetchone()

    if not record:
        print("Invalid Account Number")
        return

    stored_pin, balance = record

    if str(pin) != str(stored_pin):
        print("Invalid PIN")
        return

    withdrawal_amount = float(input("Enter amount to withdraw: "))

    if withdrawal_amount <= 0:
        print("Withdrawal amount must be positive")
        return

    if withdrawal_amount > balance:
        print("Insufficient Balance")
        return

    new_balance = balance - withdrawal_amount

    cursor.execute(
        "UPDATE Accounts SET balance = ? WHERE account_number = ?",
        (new_balance, account_num)
    )
    connect.commit()

    print("Withdrawal Successful")
    print(f"Updated Balance: ₹{new_balance}")

def account_transfer(account_num, pin):
    cursor.execute(
        "SELECT pin, balance FROM Accounts WHERE account_number = ?",
        (account_num,)
    )
    sender_record = cursor.fetchone()

    if not sender_record:
        print("Invalid Sender Account Number")
        return

    sender_pin, sender_balance = sender_record

    if str(pin) != str(sender_pin):
        print("Invalid PIN")
        return

    receiver_account = int(input("Enter Receiver Account Number: "))

    if receiver_account == account_num:
        print("Sender and Receiver accounts cannot be the same")
        return

    cursor.execute(
        "SELECT balance FROM Accounts WHERE account_number = ?",
        (receiver_account,)
    )
    receiver_record = cursor.fetchone()

    if not receiver_record:
        print("Invalid Receiver Account Number")
        return

    receiver_balance = receiver_record[0]

    transfer_amount = float(input("Enter amount to transfer: "))

    if transfer_amount <= 0:
        print("Transfer amount must be positive")
        return

    if transfer_amount > sender_balance:
        print("Insufficient Balance")
        return

    new_sender_balance = sender_balance - transfer_amount
    new_receiver_balance = receiver_balance + transfer_amount

    cursor.execute(
        "UPDATE Accounts SET balance = ? WHERE account_number = ?",
        (new_sender_balance, account_num)
    )

    cursor.execute(
        "UPDATE Accounts SET balance = ? WHERE account_number = ?",
        (new_receiver_balance, receiver_account)
    )

    connect.commit()
    print("Transfer Successful")
    print(f"Amount Transferred: ₹{transfer_amount}")
    print(f"Your Updated Balance: ₹{new_sender_balance}")

def change_pin(account_num,old_pin):
    cursor.execute("SELECT pin FROM Accounts where account_number=?",(account_num,))
    record=cursor.fetchone()
    if not record:
        print("Invalid Account Number")
        return

    stored_pin = record[0]

    if str(old_pin) != str(stored_pin):
        print("Incorrect Current PIN")
        return
    new_pin=input("Enter New 4-digit PIN:")
    confirm_pin=input("Confirm PIN:")
    if new_pin!=confirm_pin:
        print("PIN mismatch")
        return
    if new_pin == str(stored_pin):
        print("New PIN cannot be same as old PIN")
        return

    if len(new_pin)!=4 or not new_pin.isdigit():
        print("PIN must be exactly 4 digits")
        return
    cursor.execute("UPDATE Accounts SET pin=? where account_number=?",(new_pin,account_num))
    connect.commit()
    print("PIN Changed Successfully")

