import Logics.database_connector as database_connector
import Logics.book_details as book_details
import Logics.student_details as student_details
from datetime import datetime, timedelta
import Logics.input_module as i
import Logics.total_amount_taking as total_amount_taking
import Logics.send_email as sendemail

def insert_into_borrow_register(Id, borrowDetails):
# def insert_into_borrow_register(Id):
    """Inserts book and student details into the Borrow_Register table and updates stock status."""
    db_name = f"{Id}_library_db"
    connection = None
    cursor = None

    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("Failed to connect to the database.")
        return  # Use buffered cursor
    cursor = connection.cursor()
    # Get inputs from user
    # book_id = i.get_input("Enter Book ID: ")
    # student_id = i.get_input("Enter Student ID: ")
    book_id = borrowDetails["bookid"].upper()
    student_id = borrowDetails["studentid"].upper()
    print(student_id)
    # Set borrow and return dates
    query1 = """SELECT `Borrowing Period` FROM users"""
    cursor.execute(query1)
    res = cursor.fetchall()
    day = res[0][0]
    borrow_date = datetime.now().date()
    return_date = borrow_date + timedelta(days=day)
    # Set default statuses
    borrow = True
    submit = False
    renew = False
    # Fetch book and student details from database
    book = book_details.get_book_details(book_id, db_name)
    student = student_details.get_student_details(student_id, db_name)

    # Check if book or student details are missing
    if not book or not student:
        print("Cannot insert into Borrow_Register due to missing details.")
        return

    # Connect to the database
    
        
    
    try:
        # valid_payment(db_name, student_id)
        # valid_BOOKinstock(db_name, book_id)
        # valid_limiting_book(db_name, student_id)     
        cursor.execute("SELECT `Payment Functionality` FROM users")
        PF = cursor.fetchone()[0]
        # Insert borrow record
        if PF == 1:
            insert_query = """
                INSERT INTO borrowed_books
                (Book_ID, Book_Name, Author, Published_Year, Edition, Book_Price, Student_ID, Student_Name, Student_Email, Department,
                Borrow_Date, Return_Date, Payable_Amount, Borrow, Submit, Renew, Payment_Status, Reminder)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                book['Book_ID'], book['Book_Name'], book['Author'], book['Published_Year'], book['Edition'],
                book['Book_Price'], student['Student_ID'], student['Student_Name'], student['Student_Email'], student['Department'],
                borrow_date, return_date, 0.00, borrow, submit, renew, 'NOTHING TO PAY', 'NO NEED'
            ))

            # Update stock status
            update_stock_query = """
                UPDATE books
                SET Stock_Status = 'Out of Stock'
                WHERE Book_ID = %s
            """
            cursor.execute(update_stock_query, (book_id,))

            # Commit the transaction
            connection.commit()
            print(f"Student ID {student_id} has successfully borrowed Book ID {book_id}. The book's details have been added to the issue register, and the stock status has been updated accordingly.")
            if sendemail.send_library_email(cursor, student_id,book_id,"issue") == False:
                    return {"email":False}
            return {"done":True}
        else:
            cursor.execute("""SELECT Return_Date FROM borrowed_books WHERE Student_ID = %s AND Submit = 0 """, (student_id,))
            records = cursor.fetchall()
            print(records)
            today = datetime.now().date()

            # Check if any Return_Date matches today
            if any((r[0] == today or r[0] < today) for r in records if r[0] is not None):
                return {"block" : False}
            
            insert_query = """
                INSERT INTO borrowed_books
                (Book_ID, Book_Name, Author, Published_Year, Edition, Book_Price, Student_ID, Student_Name, Student_Email, Department,
                Borrow_Date, Return_Date, Payable_Amount, Borrow, Submit, Renew, Payment_Status, Reminder)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                book['Book_ID'], book['Book_Name'], book['Author'], book['Published_Year'], book['Edition'],
                book['Book_Price'], student['Student_ID'], student['Student_Name'], student['Student_Email'], student['Department'],
                borrow_date, return_date, 0.00, borrow, submit, renew, 'PAYMENT FUNCTION IS DISABLE', 'NO NEED'
            ))

            # Update stock status
            update_stock_query = """
                UPDATE books
                SET Stock_Status = 'Out of Stock'
                WHERE Book_ID = %s
            """
            cursor.execute(update_stock_query, (book_id,))

            # Commit the transaction
            connection.commit()
            print(f"Student ID {student_id} has successfully borrowed Book ID {book_id}. The book's details have been added to the issue register, and the stock status has been updated accordingly.")
            if sendemail.send_library_email(cursor, student_id,book_id,"issue") == False:
                return {"email":False}
            return {"done":True}
    except Exception as e:
        print(f"Error inserting into Borrow_Register: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
            # print("Database connection closed.")

# Call the function
# insert_into_borrow_register('672554')

def valid_payment(Id, borrowDetails):
    db_name = f"{Id}_library_db"
    student_id = borrowDetails["studentid"].upper()
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("Failed to connect to the database.")
        return  # Use buffered cursor
    cursor = connection.cursor()
    cursor.execute("SELECT `Payment Functionality` FROM users WHERE Id = %s", (Id,))
    amounts = cursor.fetchone()[0]
    if amounts == 1:
        amount = total_amount_taking.fatch_amount(db_name, student_id)
        print(amount)  
        if amount > 0:
            print(f"Student {student_id} is blocked due to non-payment.")
            # payment_API.open_payment_page()
            return False
        else:
            return True 
    else:
        return True

def getstudentdetails(Id, studentID):
    connection = None
    cursor = None
    try:
        connection = database_connector.connect_to_db(Id)
        if not connection:
            return False
        
        else:
            cursor = connection.cursor()
            # book_query = 
            cursor.execute('''SELECT Student_Name, Department, Admission_Year FROM students WHERE Student_ID = %s''', (studentID.upper(),))
            student_row = cursor.fetchone()

            Student_Name, Department, Admission_Year = student_row
            
            if not student_row:
                print("Book details not found.")
                return False
            else:
                print(Student_Name, Department, Admission_Year)
                return {"studentname": Student_Name, "Department": Department,"admissionyear": Admission_Year}
    except Exception as e:
        print(f"[Error] {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
def valid_BOOKinstock(Id, borrowDetails):
    db_name = f"{Id}_library_db"
    book_id = borrowDetails["bookid"].upper()
    
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("Failed to connect to the database.")
        return  # Use buffered cursor
    cursor = connection.cursor()
    can_borrow_query = """SELECT Stock_Status FROM books WHERE Book_ID = %s """
    cursor.execute(can_borrow_query, (book_id,))
    book_record = cursor.fetchone()
    
    if book_record[0] == 'In Stock':
        # print(f"Book ID {book_id} is already borrowed or out of stock.")
        return True
    else:
        return False
    
def valid_limiting_book(Id, borrowDetails):
    student_id = borrowDetails["studentid"].upper()
    db_name = f"{Id}_library_db"
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("Failed to connect to the database.")
        return  # Use buffered cursor
    cursor = connection.cursor()
    borrowing_check_query = """
        SELECT COUNT(*) FROM borrowed_books
        WHERE Student_ID = %s AND Borrow = TRUE
    """
    cursor.execute(borrowing_check_query, (student_id,))
    borrowed_count = cursor.fetchone()[0]
    no_of_book_allotted = ''' SELECT Number_of_books FROM users WHERE Id = %s'''
    cursor.execute(no_of_book_allotted, (Id,))
    book_allotted = cursor.fetchone()

    if borrowed_count == book_allotted[0]:
        print(f"Student ID {student_id} has reached the borrowing limit of 3 books.")
        return False
    else:
        return True
    

def valid_Books(Id, borrowDetails):
    db_name = f"{Id}_library_db"
    book_id = borrowDetails["bookid"].upper()
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("Failed to connect to the database.")
        return
    cursor = connection.cursor()

    # Query to fetch all Book_IDs
    query1 = """SELECT Book_ID FROM books"""
    cursor.execute(query1)
    results = cursor.fetchall()

    # Check if book_id exists
    if any(book_id == result[0] for result in results):
        print("yes")
        return True
    else:
        print("Book ID not found.")
        return False
    
def valid_Students(Id, borrowDetails):
    db_name = f"{Id}_library_db"
    student_id = borrowDetails["studentid"].upper()
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("Failed to connect to the database.")
        return
    cursor = connection.cursor()

    # Query to fetch all Book_IDs
    query1 = """SELECT Student_ID FROM students"""
    cursor.execute(query1)
    results = cursor.fetchall()

    # Check if book_id exists
    if any(student_id == result[0] for result in results):
        print("yes")
        return True
    else:
        print("no")
        return False
    


# ============================================================================================================================================

from datetime import datetime
import Logics.database_connector as database_connector
def valid_Teachers(Id, borrowDetails):
    """
    Validates whether the provided teacher ID exists in the 'teachers' table.
    """
    db_name = f"{Id}_library_db"
    teacher_id = borrowDetails["teacherid"].upper()  # 'studentid' is reused as input field

    # Connect to the database
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("❌ Failed to connect to the database.")
        return False

    cursor = connection.cursor()
    try:
        # Fetch all teacher IDs
        query = "SELECT Teacher_ID FROM teachers"
        cursor.execute(query)
        results = cursor.fetchall()

        # Validate the given teacher ID
        if any(teacher_id == result[0] for result in results):
            print(f"✅ Valid Teacher ID: {teacher_id}")
            return True
        else:
            print(f"❌ Invalid Teacher ID: {teacher_id}")
            return False
    except Exception as e:
        print(f"❌ Error during teacher validation: {e}")
        return False

   


def get_teacher_details(db_name,teacher_id):
    """Fetches teacher details from the Teachers table based on Teacher_ID."""
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("❌ Failed to connect to MySQL.")
        return None

    cursor = connection.cursor()
    try:
        query = """
            SELECT Teacher_ID, Teacher_Name, Teacher_Email, Designation, Department 
            FROM Teachers
            WHERE Teacher_ID = %s
        """
        cursor.execute(query, (teacher_id,))
        result = cursor.fetchone()
        if result:
            teacher_details = {
                "Teacher_ID": result[0],
                "Teacher_Name": result[1],
                "Teacher_Email": result[2],
                "Designation" : result[3],
                "Department": result[4]
            }
            print(f"✅ Teacher Details: {teacher_details}")
            return teacher_details
        else:
            print(f"❌ No teacher found with Teacher_ID {teacher_id}.")
            return None
    except Exception as e:
        print(f"❌ Error fetching teacher details: {e}")
        return None
    


def insert_into_teacher_borrow_register(Id, borrowDetails):
    """
    Inserts book and teacher details into the borrowed_books table and updates stock status.
    For teacher use only (no Payment_Status or Reminder).
    """
    db_name = f"{Id}_library_db"
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("❌ Failed to connect to the database.")
        return False

    cursor = connection.cursor()
    book_id = borrowDetails["bookid"].upper()
    teacher_id = borrowDetails["teacherid"].upper()  # Reused for teacher

    print(f"➡ Issuing Book_ID: {book_id} to Teacher_ID: {teacher_id}")

    borrow_date = datetime.now().date()
    borrow = True
    submit = False

    # Fetch details
    book = book_details.get_book_details(book_id, db_name)
    teacher = get_teacher_details(db_name,teacher_id)

    if not book or not teacher:
        print("❌ Missing book or teacher details. Cannot proceed.")
        return False

    try:
        cursor.execute("SELECT Employment_Status FROM teachers WHERE Teacher_ID = %s",(teacher_id,))
        exteacher = cursor.fetchone()[0]
        print(exteacher)
        if exteacher == "EX-TEACHER":
            return {"ex": False}
        
        insert_query = """
            INSERT INTO teacher_borrowed_books (
                Book_ID, Book_Name, Author, Published_Year, Edition, Book_Price,
                Teacher_ID, Teacher_Name, Department,
                Borrow_Date, Borrow, Submit
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            book['Book_ID'], book['Book_Name'], book['Author'], book['Published_Year'],
            book['Edition'], book['Book_Price'],
            teacher['Teacher_ID'], teacher['Teacher_Name'], teacher['Department'],
            borrow_date, borrow, submit
        ))

        update_stock_query = """
            UPDATE books
            SET Stock_Status = 'Out of Stock'
            WHERE Book_ID = %s
        """
        cursor.execute(update_stock_query, (book_id,))
        connection.commit()

        print(f"✅ Book ID {book_id} issued to Teacher ID {teacher_id}. Stock updated.")
        return True

    # except Exception as e:
    #     print(f"❌ Error inserting into borrow register: {e}")
    #     return False

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
