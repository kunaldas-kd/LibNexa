
import Logics.database_connector as database_connector
import Logics.registration as registration
import threading
import bcrypt
import logging
import Dashboard_API as dashboard_API
import Logics.REMINDER_EMAIL as REMINDER_EMAIL
import backup
import time


def create_user(Id, password):
    """Creates a new user with hashed password."""
    connection = database_connector.connect_to_db('Admin_Interface')
    if connection is None:
        print("Failed to connect to MySQL.")
        return
    cursor = connection.cursor()
    try:
        registration.insert_library_info(Id, password)
        login_user(Id, password)
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        cursor.close()
        connection.close()

def login_user(Id, password):
    """Verifies user credentials."""
    connection = database_connector.connect_to_db(f"{Id}_library_db")
    if connection is None:
        logging.error("Failed to connect to MySQL.")
        return None
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT Passwords FROM users WHERE Id = %s", (Id,))
        stored_password = cursor.fetchone()
        hashed_password = bcrypt.hashpw(stored_password[0].encode('utf-8'), bcrypt.gensalt())
        # print(f"Hashed Password: {hashed_password}")

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            print("\nLogin successful!")
            start_background_tasks(Id)
            access_library_database(Id)
            dashboard_API.open_dashboard(Id)
            return True
        else:
            print("Invalid credentials!")
            return False
    except Exception as e:
        logging.error(f"Error logging in: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def access_library_database(Id):
    """Access the user's library database after successful login."""
    connection = database_connector.connect_to_db('Admin_Interface')
    if connection is None:
        logging.error("Failed to connect to MySQL.")
        return None
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT Library_name FROM id_pass WHERE Id = %s", (Id,))
        result = cursor.fetchone()
        if result is None:
            logging.error(f"No user found with ID {Id}")
            return False
        name = result[0]
    # except Exception as e:
    #     logging.error(f"Error accessing database: {e}")
    #     return False
    finally:
        cursor.close()
        connection.close()

    print(f"\nWelcome {name}! You have access to your library database.")



# login_user('378649','378649')
def start_background_tasks(username):
    """Starts background threads for reminders and backup"""
    try:
        threading.Thread(target=REMINDER_EMAIL.MAIN_REMINDER_1, args=(username,), daemon=True).start()
        threading.Thread(target=REMINDER_EMAIL.MAIN_REMINDER_2, args=(username,), daemon=True).start()
        threading.Thread(target=backup.backup, args=(username,), daemon=True).start()
    except Exception as e:
        logging.error(f"Error while starting background tasks: {e}")