import logging
import Logics.input_module as input_module
from Logics.send_email import send_email
import Logics.database_connector as database_connector

def forgot_password(user_id):
    connection = None
    cursor = None
    connection = database_connector.connect_to_db(f"{user_id}_library_db")
    if connection is None:
        print("Failed to connect to the database.")
        return
    
    cursor = connection.cursor()  
    q = '''SELECT Library_name FROM users'''
    cursor.execute(q)
    name = cursor.fetchone()
    email, password = input_module.get_user_email_by_id(user_id)
    if email and password:

        send_email(email, user_id, password, name)
        return True
    else:
        logging.error("User not found or error retrieving user details by user id.")
        return False

def forgot_password2(email):
    user_id, password = input_module.sendpass(email)
    print(user_id)
    print(password)
    connection = None
    cursor = None
    connection = database_connector.connect_to_db(f"{user_id}_library_db")
    if connection is None:
        print("Failed to connect to the database.")
        return
    
    cursor = connection.cursor()  
    q = '''SELECT Library_name FROM users'''
    cursor.execute(q)
    name = cursor.fetchone()
    if user_id == False or password == False:
        return False
    else:
        send_email(email, user_id, password, name)
        return True
    
# forgot_password2("KUNALDAS532001@GMAIL.COM")