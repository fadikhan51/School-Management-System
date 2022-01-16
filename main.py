
from random import choice
import mysql.connector as mysql

#import os module
import os

from mysql.connector.utils import print_buffer

def clearScreen():
    operation = 'clear'
    if os.name in ('nt','dos'): 
        operation = 'cls'
    os.system(operation)


try: 
    mydb = mysql.connect(
    host = 'localhost',
    user = 'root',
    password = "",
    database = 'sms'
)
    cursor = mydb.cursor(buffered = True)

    clearScreen()
    print("\t\t\t\t\tDatabase is Connected Successfully...!")

except:
    print("Database not connected :(")

def reg_std():
    print("")
    print("\t\t\t\t\t\tRegister New Student\n")

    username = input("Enter the username to assign :")
    password = input("Enter the password to assign :")

    db_val = (username, password)

    cursor.execute("INSERT INTO users (username,password,role) VALUES (%s,%s,'student')",db_val)
    mydb.commit()

    print(username +' has been registered as a student.')

def reg_tch():
    print("")
    print("\t\t\t\t\t\tRegister New Teacher\n")

    username = input("Enter the username to assign :")
    password = input("Enter the password to assign :")

    db_val = (username, password)

    cursor.execute("INSERT INTO users (username,password,role) VALUES (%s,%s,'teacher')",db_val)
    mydb.commit()

    print(username +' has been registered as a teacher.')

def del_std():
    print("")
    print("\t\t\t\t\t\tDelete Existing Student\n")

    username = input("Enter the username of the student to delete :")
    db_val = (username,'student')

    cursor.execute("DELETE FROM users WHERE username = %s AND role = %s", db_val)
    mydb.commit()
    if cursor.rowcount < 1 :
                print("No such user found.")
    else :
                print(username + " has been deleted.")

def del_tch():
    print("")
    print("\t\t\t\t\t\tDelete Existing Teacher\n")

    username = input("Enter the username of the Teacher to delete :")
    db_val = (username,'teacher')

    cursor.execute("DELETE FROM users WHERE username = %s AND role = %s", db_val)
    mydb.commit()
    if cursor.rowcount < 1 :
                print("No such user found.")
    else :
                print(username + " has been deleted.")

def admin_func():
    while 1:
        # print("")
        print("Admin Menu\n")
        print("1. Register new Student")
        print("2. Register new Teacher")
        print("3. Delete Existing Student")
        print("4. Delete Existing Teacher")
        print("5. Logout")

        user_choice = input('\nEnter your choice:')

        if user_choice == "1":
            reg_std()

        if user_choice == "2":
            reg_tch()

        if user_choice == "3":
            del_std()

        if user_choice == "4":
            del_tch()

        if user_choice == "5":
            print("")
            break

def tch_func():
    while 1:
        print("")
        print("\t\t\t\t\tTeacher's Menu")
        print("1. Mark student register")
        print("2. View register")
        print("3. Logout")

        user_choice = input("Enter your Choice :")

        if user_choice == "1":
            print("")
            print("Mark student register\n")
            cursor.execute("SELECT username FROM users WHERE role = 'student'")
            records = cursor.fetchall()
            date    = input(str("Date : DD/MM/YYYY : "))
            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
                #Present | Absent | Late
                status = input(str("Status for " + str(record) + " P/A/L : "))
                db_val = (str(record),date,status)
                cursor.execute("INSERT INTO attendance (username, date, status) VALUES(%s,%s,%s)",db_val)
                mydb.commit()
                print(record + " Marked as " + status)

        if user_choice == "2":
            print("")
            print("\t\t\t\t\tViewing all student registers")
            cursor.execute("SELECT username, date, status FROM attendance")
            records = cursor.fetchall()
            print("Displaying all registers")
            for record in records:
                print(record)

        if user_choice == "3":
            break
                
        # else :
        #     print("No valid option was selected.")

def tch_auth():
    print("")

    username = input("Enter your username :")
    password = input("Enter your password :")
    db_val = (username,password)

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND role = 'teacher'",db_val)

    if cursor.rowcount < 1:
        print("Invalid Credentials.\n")
    else :
        tch_func()
        # print("Welcome Teacher.")

def admin_auth():
    print("")
    username = input("Enter your usrename :")
    password = input("Enter your password:")

    if username == "username":
        if password == "password":
            admin_func()
            # print("Logged in as Admin.\n")
        else :
            print("Invalid Password.\n")
    else :
        print("Invalid credentials.\n")

def std_auth():
    print("")
    print("Student's Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    db_val = (username, password, "student")
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND role = %s",db_val)
    if cursor.rowcount <= 0:
        print("Invalid login details")
    else:
        std_func(username)

def std_func(username):
     while 1:
        print("")
        print("Student's Menu")
        print("")
        print("1. View Register")
        print("2. Download Register")
        print("3. Logout")

        user_option = input(str("Option : "))
        
        if user_option == "1":
            print("Displaying register")
            username = (str(username),)             #why we used , and what is username
            cursor.execute("SELECT date, username, status FROM attendance WHERE username = %s",username)
            records = cursor.fetchall()
            for record in records:
                print(record)

        elif user_option == "2":
            print("Downloading Register")
            username = (str(username),)
            cursor.execute("SELECT date, username, status FROM attendance WHERE username = %s",username)
            records = cursor.fetchall()
            for record in records:
                with open("C:/Users/fk203/Desktop/register.txt", "w") as f:   # w is used for write
                    f.write(str(records)+"\n")
                f.close()
            print("All records saved")

        elif user_option == "3":
            break

        else:
            print("No valid option was selected")


print('\n\n')
print("\t\t\t\t\t Welcome to School Management System")


# Login Page
def main():
    while 1:
        print("1. Login as Student.")
        print("2. Login as Teacher.")
        print("3. Login as Admin.")

        user_choice = input('\nEnter your choice:')

        if user_choice == "1":
            std_auth()
        elif user_choice == "2":
            tch_auth()
        elif user_choice == "3":
            admin_auth()
        else :
            print("\nInvalid choice.")
main()