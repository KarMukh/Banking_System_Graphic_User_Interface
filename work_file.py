

# This is a work file, trying to finish up first with transfer part and then with delete account, modify, etc.


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
                Button(accounts_dashboard, text='Transfer', font=('Calibri', 12), width=30, command=transfer).grid(row=5, sticky=N, padx=10)
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


def transfer():
    # print('Transfer')
    # global withdraw_user_name
    global temp_transfer_user_name
    global transfer_amount
    global transfer_notification
    global current_balance1_tag
    global current_balance2_tag
    # global file1
    # global file2
    # global username1
    # global username2

    # withdraw_user_name = StringVar()
    temp_transfer_user_name = StringVar()
    transfer_amount = StringVar()
    file1 = open(login_name, 'r')
    file1_data = file1.read()
    user1_details = file1_data.split('\n')
    details_name1 = user1_details[0]
    details_balance1 = user1_details[4]

    transfer_screen = Toplevel(master)
    transfer_screen.title('Transfer')

    Label(transfer_screen, text='Transfer', font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    current_balance1_tag = Label(transfer_screen, text=details_name1+"'s "+'Current Balance is : $'+ details_balance1, font=('Calibri', 12))
    current_balance1_tag.grid(row=1, sticky=W)
    Label(transfer_screen, text='Transfer User Name', font=('Calibri', 12)).grid(row=3, sticky=W)
    Label(transfer_screen, text='Transfer Amount', font=('Calibri', 12)).grid(row=4, sticky=W)
    transfer_notification = Label(transfer_screen, font=('Calibri', 12))
    transfer_notification.grid(row=5, sticky=N, pady=5)

    # Entry(transfer_screen, textvariable=withdraw_user_name).grid(row=2, column=1)
    Entry(transfer_screen, textvariable=temp_transfer_user_name).grid(row=3, column=1)
    Entry(transfer_screen, textvariable=transfer_amount).grid(row=4, column=1)
    # ow=2, column=1 cause I want the entry to be on the same level as Label for it
    # if file1 != file2:
    # file2 = open(transfer_user_name, 'r')
    # file2_data = file2.read()
    # user2_details = file2_data.split('\n')
    # details_name2 = user2_details[0]
    # details_balance2 = user2_details[4]

    # transfer_screen = Toplevel(master)
    # transfer_screen.title('Transfer2')

    # Label(transfer_screen, text='Transfer2', font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    # current_balance2_tag = Label(transfer_screen, text='Current Balance : $'+details_balance2, font=('Calibri', 12))
    # current_balance2_tag.grid(row=2, sticky=W)

    Button(transfer_screen, text='Finish', font=('Calibri', 12), command=finish_transfer).grid(row=6, sticky=W, pady=5)


def finish_transfer():

    # listdir returns a list containing the names of the files in the directory.
    # for name in all_accounts:
    #     username1 = input("Enter user name to withdraw from ")
    #     if name != username1:
    #         notification.config(fg='red', text="Wrong username1 is inputted")

    if transfer_amount.get() == "":
        transfer_notification.config(text="Transfer amount is required!", fg='red')

    if float(transfer_amount.get()) <= 0:
        transfer_notification.config(text="0 or negative currency is not accepted", fg='red')
        return
    file1 = open(login_name, 'r+')
    file1_data = file1.read()
    details1 = file1_data.split('\n')
    details_name1 = details1[0]
    current_balance1 = details1[4]
    if float(transfer_amount.get()) > float(current_balance1):
        transfer_notification.config(text='Insufficient Funds!', fg='red')
        return
    updated_balance1 = current_balance1
    updated_balance1 = float(updated_balance1) - float(transfer_amount.get())
    file1_data = file1_data.replace(current_balance1, str(updated_balance1))
    file1.seek(0)
    file1.truncate(0)
    file1.write(file1_data)
    file1.close()

    current_balance1_tag.config(text="Current Balance : $"+str(updated_balance1), fg='green')
    # return
    # global transfer_user_name
    all_accounts = os.listdir()
    transfer_user_name = temp_transfer_user_name.get()
    for name in all_accounts:
        # transfer_user_name = input("Enter user name to transfer to ")
        if name == transfer_user_name: # and transfer_user_name != details_name1
            # if file1 != file2:
            file2 = open(transfer_user_name, 'r+')
            file2_data = file2.read()
            details2 = file2_data.split('\n')
            transfer_user_name = details2[0]
            current_balance2 = details2[4]

            # if transfer_user_name != details_name1 and transfer_user_name == details2[0]:
                # if float(withdraw_amount.get()) > float(current_balance1):
                #     withdraw_notification.config(text='Insufficient Funds!', fg='red')
                #     return
            updated_balance2 = current_balance2
            updated_balance2 = float(updated_balance2) + float(transfer_amount.get())
            file2_data = file2_data.replace(current_balance2, str(updated_balance2))
            file2.seek(0)
            file2.truncate(0)
            file2.write(file2_data)
            file2.close()

    # current_balance2_tag.config(text="Current Balance : $" + str(updated_balance2), fg='green')

            transfer_notification.config(text="Both balances are updated", fg='green')
        else:
            transfer_notification.config(fg='red', text="Wrong user_name2 is inputted")

######### փորձեմ վիդրո ֆուլլ ֆունկցիա ու դեպոզիտ

######### առաջին պատուհանում վիդրով անոըն ու տրանսֆեր գումար հետո երկրորդ պատուհան տրասֆեր անուն ու եթե ճիշտ է առաջինից մինուս երկրորդին պլյուս

    # file1 = open(login_name, 'r+')
    # file2 = open(login_name, 'r+')
    #
    # ################### files are matched cause balances are the same
    #
    # #### and no entries for name1, name1 and transfer_amount
    #
    # file1 != file2
    # # or
    # name1 != name2
    #
    # file1_data = file1.read()
    # file2_data = file2.read()
    #
    # details1 = file1_data.split('\n')
    # details2 = file2_data.split('\n')
    #
    # name1 = details1[0]
    # name2 = details2[0]
    #
    # current_balance1 = details1[4]
    # current_balance2 = details2[4]
    #
    # if float(transfer_amount.get()) > float(current_balance1):
    #     transfer_notification.config(text='Insufficient Funds!', fg='red')
    #     return
    # updated_balance1 = current_balance1
    # updated_balance1 = float(updated_balance1) - float(transfer_amount.get())
    # updated_balance2 = current_balance2
    # updated_balance2 = float(updated_balance2) + float(transfer_amount.get())
    #
    # file1_data = file1_data.replace(current_balance1, str(updated_balance1))
    # file2_data = file2_data.replace(current_balance2, str(updated_balance2))
    #
    # file1.seek(0)
    # file1.truncate(0)
    # file1.write(file1_data)
    # file1.close()
    #
    # file2.seek(0)
    # file2.truncate(0)
    # file2.write(file2_data)
    # file2.close()
    #
    # current_balance1_tag.config(text="Current Balance : $"+str(updated_balance1), fg='green')
    # current_balance2_tag.config(text="Current Balance : $" + str(updated_balance2), fg='green')
    #
    # transfer_notification.config(text="Both balances are updated", fg='green')


# def check(entry):
    #     search = open('all_accounts', 'r')
    #     if str(entry) in str(search):
    #         return (entry, "Word found")
    #     else:
    #         return entry, ("Word not found")

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



        # C:\Users\KarenM\Documents\Python\Flask\Banking_System_GUI\Scripts\python.exe C:\Users\KarenM\PycharmProjects\Banking_System_GUI\main.py
        # Exception in Tkinter callback
        # Traceback (most recent call last):
        #   File "C:\Users\KarenM\AppData\Local\Programs\Python\Python311\Lib\tkinter\__init__.py", line 1948, in __call__
        #     return self.func(*args)
        #            ^^^^^^^^^^^^^^^^
        #   File "C:\Users\KarenM\PycharmProjects\Banking_System_GUI\main.py", line 205, in finish_withdraw
        #     file.truncate(0)
        # io.UnsupportedOperation: truncate

        # Exception in Tkinter callback
        # Traceback (most recent call last):
        #   File "C:\Users\KarenM\AppData\Local\Programs\Python\Python311\Lib\tkinter\__init__.py", line 1948, in __call__
        #     return self.func(*args)
        #            ^^^^^^^^^^^^^^^^
        #   File "C:\Users\KarenM\PycharmProjects\Banking_System_GUI\main.py", line 149, in finish_deposit
        #     file.truncate(0)
        # io.UnsupportedOperation: truncate


""" Այս էռոռները տալիս էր, քանի որ finish_deposit և finish_withdraw ֆուկնցիաներում file = open(login_name, 'r+') տողում
'r+'-ի փոխարեն 'r' էի դնում ու read and write -ի փոխարեն մենակ read էր անում """