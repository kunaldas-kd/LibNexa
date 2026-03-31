import Logics.database_connector as database_connector
from datetime import timedelta, datetime
import time
import Logics.send_email as send_email

def reminder1(Id):
    # Connect to the database
    user_db_name = f"{Id}_library_db"
    connection = database_connector.connect_to_db(user_db_name)
    if connection is None:
        print("Failed to connect to the database.")
        return

    # Set to track reminders already sent (stored as tuples of Student_ID and Return_Date)
    
    try:
        # while True:
        cursor = connection.cursor()
        query = '''
            SELECT Library_name, Institute_Email, `Late Fine Amount` FROM users 
        '''
        cursor.execute(query)
        result = cursor.fetchone()
        libraryname = result[0]
        contact = result[1].lower()
        amount = result[2]
        # print(result)
        # Query to get all unsubmitted return dates along with student details
        query1 = '''
            SELECT Student_ID, Student_Name, Student_Email, Book_Name, Return_Date 
            FROM borrowed_books 
            WHERE Submit = 0 AND Reminder = 'NO NEED'
        '''
        cursor.execute(query1)
        borrowed_books = cursor.fetchall()  # Fetch all results
        # sent_reminders.add((student_id, return_date))
        if borrowed_books:
            for student_id, Student_Name, student_email, book_name, return_date in borrowed_books:
                # Calculate the send time               
                send_time = return_date - timedelta(days=3)
                now = datetime.now().date()

                # Check if the reminder has already been sent
                if now >= send_time :
                    print(f"Sending reminder to Student ID: {student_id}, Email: {student_email}...")
                    
                    # Simulate sending an email (replace with real email logic)
                    email = send_email.send_reminder_email_1(student_email, Student_Name, book_name,amount, libraryname, contact)
                    print(email)
                    if email == True : 
                    # Add to sent_reminders to avoid duplicate emails
                        r_d = send_time + timedelta(days=3)
                        print(r_d)
                        query5 = '''UPDATE borrowed_books
                                        SET Reminder = %s
                                        WHERE Student_ID = %s AND Return_Date = %s'''
                        data5 = 'Reminder Sent 1', student_id, r_d
                        cursor.execute(query5, data5)
                        connection.commit()
                    else:
                        return
                    
        
        else:
            return

        # Sleep before the next check
        time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
# reminder1("508435")

def reminder2(Id):

    # Connect to the database
    user_db_name = f"{Id}_library_db"
    connection = database_connector.connect_to_db(user_db_name)
    if connection is None:
        print("Failed to connect to the database.")
        return

    # Set to track reminders already sent (stored as tuples of Student_ID and Return_Date)
    
    try:
        # while True:
        cursor = connection.cursor()
        query = '''
            SELECT Library_name, Institute_Email, `Late Fine Amount` FROM users 
        '''
        cursor.execute(query)
        result = cursor.fetchone()
        libraryname = result[0]
        contact = result[1].lower()
        amount = result[2]
        # print(result)
        # Query to get all unsubmitted return dates along with student details
        query1 = '''
            SELECT Student_ID, Student_Name, Student_Email, Book_Name, Return_Date 
            FROM borrowed_books 
            WHERE Submit = 0 AND Reminder = 'Reminder Sent 1'
        '''
        cursor.execute(query1)
        borrowed_books = cursor.fetchall()  # Fetch all results
        # sent_reminders.add((student_id, return_date))
        if borrowed_books:
            for student_id, Student_Name, student_email, book_name, return_date in borrowed_books:
                # Calculate the send time               
                send_time = return_date
                now = datetime.now().date()

                # Check if the reminder has already been sent
                if now > send_time :
                    print(f"Sending reminder to Student ID for date over: {student_id}, Email: {student_email}...")
                    
                    # Simulate sending an email (replace with real email logic)
                    email = send_email.send_reminder_email_2(student_email, Student_Name, book_name, amount, send_time, libraryname, contact)

                    # Add to sent_reminders to avoid duplicate emails
                    if email == True:
                        query5 = '''UPDATE borrowed_books
                                        SET Reminder = %s
                                        WHERE Student_ID = %s AND Return_Date = %s '''
                        data5 = 'Reminder Sent 2', student_id, send_time
                        cursor.execute(query5, data5)
                        connection.commit()
                    else:
                        return False
        
        else:
            return

        # Sleep before the next check
        time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()



def MAIN_REMINDER_1(ID):
    while True:
        reminder1(ID)
    
def MAIN_REMINDER_2(ID):
    while True:
        reminder2(ID)
        

# MAIN_REMINDER_1("508435")