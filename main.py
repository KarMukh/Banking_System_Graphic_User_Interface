from tkinter import *
import os
from PIL import ImageTk, Image

master = Tk()
master.title('Banking System App')


def register():
    global temp_name
    global temp_age
    global temp_gender
    global temp_password
    global notification
    temp_name = StringVar()
    temp_age = StringVar()
    temp_gender = StringVar()
    temp_password = StringVar()

    register_screen = Toplevel(master)
    register_screen.title('Register')

    Label(register_screen, text="Please enter your details below to register", font=('Calibri', 13)).grid(row=0, sticky=N, pady=10)
    Label(register_screen, text="Name", font=('Calibri', 13)).grid(row=1, sticky=W)
    Label(register_screen, text="Age", font=('Calibri', 13)).grid(row=2, sticky=W)
    Label(register_screen, text="Gender", font=('Calibri', 13)).grid(row=3, sticky=W)
    Label(register_screen, text="Password", font=('Calibri', 13)).grid(row=4, sticky=W)
    notification = Label(register_screen, font=('Calibri', 12))
    notification.grid(row=6, sticky=N, pady=10)

    Entry(register_screen, textvariable=temp_name).grid(row=1, column=0)
    Entry(register_screen, textvariable=temp_age).grid(row=2, column=0)
    Entry(register_screen, textvariable=temp_gender).grid(row=3, column=0)
    Entry(register_screen, textvariable=temp_password, show='*').grid(row=4, column=0)

    Button(register_screen, text='Register', command=finish_registration, font=('Calibri', 12)).grid(row=5, sticky=N, pady=10)


def finish_registration():
    # print('done')
    name = temp_name.get()
    age = temp_age.get()
    gender = temp_gender.get()
    password = temp_password.get()
    all_accounts = os.listdir()
    # print(all_accounts)
    if name == "" or age == "" or gender == "" or password == "":
        notification.config(fg='red', text="All fields are required")
        return
    for name_check in all_accounts:
        if name == name_check:
            notification.config(fg='red', text="Account already exists")
            return
        else:
            new_file = open(name, "w")
            new_file.write(name+'\n')
            new_file.write(password+'\n')
            new_file.write(age+'\n')
            new_file.write(gender+'\n')
            new_file.write('0')
            # new_file.write('0') this one is for balance, cause on the start the balance is 0
            new_file.close()
            notification.config(fg='green', text="Account has been created")


def login_session():
    global login_name
    # print('session')
    all_accounts = os.listdir()
    login_name = temp_login_name.get()
    login_password = temp_login_password.get()

    for name in all_accounts:
        if name == login_name:
            # print('Account exists!')
            file = open(name, 'r')
            file_data = file.read()
            file_data = file_data.split('\n')
            password = file_data[1]
            # We get a list with name, password, age, gender and balance in it.
            # So the position for password in that list is 1.
            if login_password == password:
                login_screen.destroy()
                accounts_dashboard = Toplevel(master)
                accounts_dashboard.title('Dashboard')

                Label(accounts_dashboard, text="Account Dashboard", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
                Label(accounts_dashboard, text="Welcome "+name, font=('Calibri', 12)).grid(row=1, sticky=N, pady=5)

                Button(accounts_dashboard, text='Personal Details', font=('Calibri', 12), width=30, command=personal_details).grid(row=2, sticky=N, padx=10)
                Button(accounts_dashboard, text='Deposit', font=('Calibri', 12), width=30, command=deposit).grid(row=3, sticky=N, padx=10)
                Button(accounts_dashboard, text='Withdraw', font=('Calibri', 12), width=30, command=withdraw).grid(row=4, sticky=N, padx=10)
                Label(accounts_dashboard).grid(row=5, sticky=N, pady=10)
                # The last one gonna leave a bit of space for us.
            # print(file_data)
                return
            else:
                login_notification.config(fg="red", text='Password is not correct!')
            return
    login_notification.config(fg="red", text='No such an account found!')
    # When the username or password are not recognized.


def deposit():
    # print('Deposit')
    global amount
    global deposit_notification
    global current_balance_tag
    amount = StringVar()
    file = open(login_name, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]

    deposit_screen = Toplevel(master)
    deposit_screen.title('Deposit')

    Label(deposit_screen, text='Deposit', font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    current_balance_tag = Label(deposit_screen, text='Current Balance : $'+details_balance, font=('Calibri', 12))
    current_balance_tag.grid(row=1, sticky=W)
    Label(deposit_screen, text='Amount', font=('Calibri', 12)).grid(row=2, sticky=W)
    deposit_notification = Label(deposit_screen, font=('Calibri', 12))
    deposit_notification.grid(row=4, sticky=N, pady=5)

    Entry(deposit_screen, textvariable=amount).grid(row=2, column=1)
    # ow=2, column=1 cause I want the entry to be on the same level as Label for it

    Button(deposit_screen, text='Finish', font=('Calibri', 12), command=finish_deposit).grid(row=3, sticky=W, pady=5)


def finish_deposit():
    if amount.get() == "":
        deposit_notification.config(text="Amount is required!", fg='red')
    if float(amount.get()) <= 0:
        deposit_notification.config(text="0 or negative currency is not accepted", fg='red')
        return

    file = open(login_name, 'r+')
    # r+ means we can both read and write
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]
    updated_balance = current_balance
    updated_balance = float(updated_balance) + float(amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    # replace is a function which looks for a str and replace it whatever we mention
    # here replace finds current_balance string and replace it with another string converted updated_balance
    # to overwrite the file following need to be done:
    file.seek(0)
    file.truncate(0)
    # The truncate() method resizes the file to the given number of bytes.
    # If the size is not specified, the current position will be used.
    # 0 because I need to start from 0
    file.write(file_data)
    # here the most recent and overwritten file_data most recent balance gonna be stored
    file.close()

    current_balance_tag.config(text="Current Balance : $"+str(updated_balance), fg='green')
    deposit_notification.config(text="Balance Updated", fg='green')


def withdraw():
    # print('Withdraw')
    global withdraw_amount
    global withdraw_notification
    global current_balance_tag
    withdraw_amount = StringVar()
    file = open(login_name, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]

    withdraw_screen = Toplevel(master)
    withdraw_screen.title('Withdraw')

    Label(withdraw_screen, text='Withdraw', font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    current_balance_tag = Label(withdraw_screen, text='Current Balance : $' + details_balance, font=('Calibri', 12))
    current_balance_tag.grid(row=1, sticky=W)
    Label(withdraw_screen, text='Withdraw Amount', font=('Calibri', 12)).grid(row=2, sticky=W)
    withdraw_notification = Label(withdraw_screen, font=('Calibri', 12))
    withdraw_notification.grid(row=4, sticky=N, pady=5)

    Entry(withdraw_screen, textvariable=withdraw_amount).grid(row=2, column=1)

    Button(withdraw_screen, text='Withdraw', font=('Calibri', 12), command=finish_withdraw).grid(row=3, sticky=W, pady=5)


def finish_withdraw():
    if withdraw_amount.get() == "":
        withdraw_notification.config(text="Withdraw amount is required!", fg='red')
    if float(withdraw_amount.get()) <= 0:
        withdraw_notification.config(text="0 or negative currency is not accepted", fg='red')
        return

    file = open(login_name, 'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]
    if float(withdraw_amount.get()) > float(current_balance):
        withdraw_notification.config(text='Insufficient Funds!', fg='red')
        return
    updated_balance = current_balance
    updated_balance = float(updated_balance) - float(withdraw_amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

    current_balance_tag.config(text="Current Balance : $"+str(updated_balance), fg='green')
    withdraw_notification.config(text="Balance Updated", fg='green')


def personal_details():
    file = open(login_name, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_name = user_details[0]
    # We don't use here user_details[1] which is the password in the list
    details_age = user_details[2]
    details_gender = user_details[3]
    details_balance = user_details[4]

    personal_details_screen = Toplevel(master)
    personal_details_screen.title('Personal Details')

    Label(personal_details_screen, text="Personal Details", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(personal_details_screen, text="Name :"+details_name, font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(personal_details_screen, text="Age :" + details_age, font=('Calibri', 12)).grid(row=2, sticky=W)
    Label(personal_details_screen, text="Gender :" + details_gender, font=('Calibri', 12)).grid(row=3, sticky=W)
    Label(personal_details_screen, text="Balance :" + details_balance, font=('Calibri', 12)).grid(row=4, sticky=W)


def login():
    global temp_login_name
    global temp_login_password
    global login_notification
    global login_screen
    temp_login_name = StringVar()
    temp_login_password = StringVar()
    # print('This is the login page')
    login_screen = Toplevel(master)
    login_screen.title('Login')

    Label(login_screen, text="Login to your account", font=('Calibri', 13)).grid(row=0, sticky=N, pady=10)
    Label(login_screen, text="Username", font=('Calibri', 11)).grid(row=1, sticky=W)
    Label(login_screen, text="Password", font=('Calibri', 11)).grid(row=2, sticky=W)
    login_notification = Label(login_screen, font=('Calibri', 13))
    login_notification.grid(row=4, sticky=W)

    Entry(login_screen, textvariable=temp_login_name).grid(row=1, column=1, padx=5)
    Entry(login_screen, textvariable=temp_login_password, show='*').grid(row=2, column=1, padx=5)

    Button(login_screen, text='Login', command=login_session, width=15, font=('Calibri', 12)).grid(row=3, sticky=W, pady=5, padx=5)


img = Image.open('3.jpg')
img = img.resize((800, 300))
img = ImageTk.PhotoImage(img)

Label(master, text="Banking System", font=('Calibri', 15), fg='purple').grid(row=0, sticky=N, pady=10)
Label(master, text="Picsart Academy Lab Projects", font=('Calibri', 12), fg='purple').grid(row=1, sticky=E)
Label(master, image=img).grid(row=2, sticky=N, pady=15)

Button(master, text='Register', font=('Calibri', 12), width=20, command=register).grid(row=3, sticky=N)
Button(master, text='Login', font=('Calibri', 12), width=20, command=login).grid(row=4, sticky=N, pady=10)

master.mainloop()
