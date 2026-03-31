import Logics.database_connector as database_connector
from datetime import datetime, timedelta
import Logics.send_email as sendmail
from Logics.total_amount_taking import fatch_amount

def submit_book(id, submitbook):
    """Updates the stock status when the book is returned."""
    # Get input from user
    book_id = submitbook["bookID"].upper()
    Student_Id = submitbook["studentid"].upper()
    # Connect to the database
    db = f"{id}_library_db"
    connection = database_connector.connect_to_db(db)
    if connection is None:
        print("Failed to connect to MySQL.")
        return
    
  
    try:
        cursor = connection.cursor()
        query1 = """SELECT Stock_Status FROM books WHERE Book_ID = %s"""
        cursor.execute(query1, (book_id,))
        record = cursor.fetchall()
        print(record[0])
        if record[0][0] == "Out of Stock":
            submit = updatesubmittedbook(connection, book_id, Student_Id)
            return submit
        else:
            print(f"No borrow record found for Book ID: {book_id} and Student ID: {Student_Id}.")
            return False
    except Exception as e:
        print(f"Error submitting book in transaction: {e}")
    finally:
        cursor.close()
        connection.close()

def renew_book(db_name,renewBookData):
    """Renews a borrowed book by updating Borrow_Date and extending Return_Date."""
    # Prompt user for Book ID and Student ID
    # book_id = input_module.get_input("Enter Book ID to renew: ")
    # student_id = input_module.get_input("Enter Student ID to renew for: ")
    book_id = renewBookData["bookID"].upper()
    student_id = renewBookData["studentid"].upper()

    # Connect to the database
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("Failed to connect to the database.")
        return

    cursor = connection.cursor()
    try:
        
        # fine_calculator.update(connection, book_id, student_id)
        # Fetch the record where Submit is zero
        query = """SELECT Payable_Amount FROM borrowed_books WHERE Book_ID = %s AND Student_ID = %s AND Submit = 0 """
        cursor.execute(query, (book_id, student_id))
        payment_status = cursor.fetchone()
        print(payment_status)
        if payment_status == None:
            print("No record has been found based on the provided information.")
            return False
        # if payment_status[0] == 'NOT PAID':
        #     print(f"Book {book_id} cannot be renewed as Student {student_id} is blocked due to non-payment.")
        #     return
        # print (payment_status[0][0])
        # if payment_status[0] == 'NOTHING TO PAY' or payment_status[0] == 'PAID':
        if payment_status[0] == 0.00:
            query1 = """SELECT Return_Date FROM borrowed_books WHERE Book_ID = %s AND Student_ID = %s AND Submit = 0 """
            cursor.execute(query1, (book_id, student_id))
            record = cursor.fetchone()
            print(record)
            if record:
             
                return_date = record[0]
                # Extend Return_Date by 15 days from the new Borrow_Date
                cursor.execute("""SELECT `Borrowing Period` FROM users""")
                period = cursor.fetchone()
                new_return_date = return_date + timedelta(days=period[0])
                # Update the borrow record in the database
                update_query = """UPDATE borrowed_books SET Borrow_Date = %s, Return_Date = %s, Renew = %s WHERE Book_ID = %s AND Student_ID = %s AND Submit = %s"""
                cursor.execute(update_query, (return_date, new_return_date, True, book_id, student_id, 0))
                # Commit the changes
                connection.commit()
                print("Book successfully renewed.")
                print(f"New Borrow Date: {return_date.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"New Return Date: {new_return_date.strftime('%Y-%m-%d %H:%M:%S')}")

                if sendmail.send_library_email(cursor, student_id, book_id,"renew")== False:
                    return {"email":False}
                return True
            # else:
                # print(f"No borrow record found for Book ID: {book_id} and Student ID: {student_id}, or the book has already been submitted and cannot be renewed.")
                # return
        # else:
            # print("Unexpected Payment Status encountered.")
    except Exception as e:
        print(f"Error renewing book in transaction: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def updatesubmittedbook(connection, book_id, Student_Id):
    cursor = connection.cursor()
    cursor.execute("SELECT `Payment Functionality` FROM users")
    amounts = cursor.fetchone()[0]
    if amounts == 1:
        # Ensure the record exists
     
        # cursor.execute("""SELECT Book_ID, Student_ID FROM borrowed_books 
        #             WHERE Book_ID = %s AND Student_ID = %s""", (book_id, Student_Id))
        # record1 = cursor.fetchone()

        # if record1:
            # Fetch all results to clear any unread results
            # cursor.fetchall()

            # Update the submission status
      
        cursor.execute("""
            UPDATE borrowed_books
            SET Submit = 1, Borrow = 0, Renew = 0
            WHERE Book_ID = %s and Student_Id = %s
        """, (book_id, Student_Id))

        # Fetch all results to clear any unread results
        cursor.fetchall()

        # Check if the book can be marked as "In Stock"
    
        cursor.execute("""
            SELECT COUNT(*) FROM borrowed_books WHERE Book_ID = %s AND Submit = 0
        """, (book_id,))
        active_borrowers = cursor.fetchone()[0]

        # Clear any unread results
        cursor.fetchall()

        if active_borrowers == 0:
            
            cursor.execute("""
                UPDATE books SET Stock_Status = 'In Stock' WHERE Book_ID = %s
            """, (book_id,))

        # Fetch all results to ensure no unread results
        cursor.fetchall()

        # Commit the transaction
        connection.commit()
        print("Book successfully submitted and stock status updated.")
        
        if sendmail.send_library_email(cursor, Student_Id, book_id,"submit")== False:
            return {"email":False}
        return {"done":True}
    else:   
        # Ensure the record exists
    # query1 = """SELECT Book_ID, Student_ID FROM borrowed_books 
    #             WHERE Book_ID = %s AND Student_ID = %s"""
    # cursor.execute(query1, (book_id, Student_Id))
    # record1 = cursor.fetchone()

    # if record1:
        # Fetch all results to clear any unread results
        cursor.fetchall()

        # Update the submission status
        cursor.execute("""UPDATE borrowed_books SET Submit = 1, Borrow = 0, Renew = 0, Payment_Status = "PAYMENT FUNCTION IS DISABLE" WHERE Book_ID = %s and Student_Id = %s""", (book_id, Student_Id))

        # Fetch all results to clear any unread results
        cursor.fetchall()

        # Check if the book can be marked as "In Stock"
        cursor.execute("SELECT COUNT(*) FROM borrowed_books WHERE Book_ID = %s AND Submit = 0", (book_id,))
        active_borrowers = cursor.fetchone()[0]

        # Clear any unread results
        cursor.fetchall()

        if active_borrowers == 0:
            cursor.execute("""
                UPDATE books SET Stock_Status = 'In Stock' WHERE Book_ID = %s
            """, (book_id,))

        # Fetch all results to ensure no unread results
        cursor.fetchall()

        # Commit the transaction
        connection.commit()
        print("Book successfully submitted and stock status updated.")
        if sendmail.send_library_email(cursor, Student_Id, book_id,"submit")== False:
            return {"email":False}
        return {"done":True}
# def valid_payment(Id, borrowDetails):
#     db_name = f"{Id}_library_db"
#     student_id = borrowDetails["studentID"].upper()
#     amount = fatch_amount(db_name, student_id)
        
#     if amount > 0.00:
#         print(f"Student {student_id} is blocked due to non-payment.")
#         # payment_API.open_payment_page()
#         return False
#     else:
#         return True
    


# submit_book('672554')
# renew_book('248903_library_db')

import Logics.database_connector as database_connector

def submit_book_teacher(id, submitbook):
    """Updates the stock status when a teacher returns a book."""
    book_id = submitbook["bookid"].upper()
    teacher_id = submitbook["teacherid"].upper()

    # Connect to the teacher's database
    db = f"{id}_library_db"
    connection = database_connector.connect_to_db(db)
    if connection is None:
        print("❌ Failed to connect to MySQL.")
        return

    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            UPDATE teacher_borrowed_books
            SET Submit = 1, Borrow = 0
            WHERE Book_ID = %s AND Teacher_ID = %s
        """, (book_id, teacher_id))

        # Check if all copies of the book are now returned
        
        cursor.execute("""
                UPDATE books SET Stock_Status = 'In Stock' WHERE Book_ID = %s
            """, (book_id,))

        connection.commit()
        print(f"✅ Book {book_id} successfully submitted by Teacher ID {teacher_id}.")
        return True
        
        

    except Exception as e:
        print(f"❌ Error in teacher book submission: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

