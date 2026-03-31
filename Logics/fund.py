import Logics.database_connector as database_connector
import Logics.Get_balance as credit
import random
from datetime import datetime

import Logics.missingbook
# import database_connector as database_connector
# import Get_balance as credit
def Credit(Id, Student, book_id, Amount, paymentType, Reason):
    connection = None
    cursor = None
    REASON = Reason.upper()

    try:
        # Establish DB connection
        connection = database_connector.connect_to_db(Id)
        if not connection:
            print("Database connection failed.")
            return False

        # Create buffered cursor to avoid "Unread result found" error
        cursor = connection.cursor(buffered=True)

        # Fetch book details
        book_query = '''
            SELECT Book_Name, Author, Published_Year, Edition, Stock_Status
            FROM books
            WHERE Book_ID = %s
        '''
        cursor.execute(book_query, (book_id,))
        book_row = cursor.fetchone()

        if not book_row:
            print("Book details not found.")
            return False

        Book_Name, Author, Published_Year, Edition, Stock_Status = book_row

        # Fetch student name
        Student_query = '''
            SELECT Student_Name
            FROM students
            WHERE Student_ID = %s
        '''
        cursor.execute(Student_query, (Student,))
        Student_row = cursor.fetchone()

        if not Student_row:
            print("Student not found.")
            return False

        Student_name = Student_row[0]
        print("Student Name:", Student_name)

        # Construct reason for transaction
        reason = f"The {Book_Name} by {Author} is {REASON} by {Student_name}"

        # if Stock_Status in ['Out of Stock', 'In Stock']:
        #     # Update book stock status
        #     update_book_query = '''
        #         UPDATE books
        #         SET Stock_Status = %s
        #         WHERE Book_ID = %s
        #     '''
        #     cursor.execute(update_book_query, (REASON, book_id))
        #     connection.commit()
        #     print("Book status updated successfully in 'books' table.")
        data = {
                "bookID": book_id,
                "reason" : REASON
            }
        Logics.missingbook.missing_book(Id, data)
        # Generate transaction ID
        combination = ''.join(str(random.randint(0, 9)) for _ in range(9))
        Transaction_ID = f"T{combination}"
        Transaction_Date = datetime.now().date()

        # Calculate new balance
        previousbalance = credit.credit(Id)
        balance = float(previousbalance)
        amount = float(Amount)
        endbalance = balance + amount

        print(f"Present Balance: {endbalance}")

        # Insert into cash_book
        insert_query = '''
            INSERT INTO cash_book (
                Transaction_ID, Student_ID, Transaction_Date, Description,
                Transaction_Type, Amount, Credit, Debit, Balance
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (
            Transaction_ID.upper(), Student.upper(), Transaction_Date, reason,
            paymentType.upper(), Amount, True, False, endbalance
        ))
        connection.commit()

        # Reset book-related flags
        insert_query_1 = '''
            UPDATE borrowed_books
            SET Borrow = %s, Submit = %s, Renew = %s
            WHERE Book_ID = %s AND Student_ID = %s
        '''
        cursor.execute(insert_query_1, (False, True, False, book_id, Student))
        connection.commit()

        print("Payment success.")
        return True

        # else:
        #     print("Book status not eligible for update.")
        #     return False

    except Exception as e:
        print("An error occurred in Payment:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
# Credit("163452_library_db", "SID1002", 9, 455, "online", "lost")

def Debit(Id, type, name, Amount, Reason):
    connection = None
    cursor = None
    try:
        connection = database_connector.connect_to_db(Id)
        if not connection:
            return False
        
        else:
            cursor = connection.cursor()
            combination = ''.join(str(random.randint(0, 9)) for _ in range(9))
            Transaction_ID = f"T{combination}"
            
            Transaction_Date = datetime.now().date()
            
            previousbalance = credit.credit(Id)
            balance = float(previousbalance)
            endbalance = balance - Amount
            person = f"{name} ({type})"

            print(f"PRESENT BALANCE {endbalance}")
            insert_query = '''
                INSERT INTO cash_book (
                    Transaction_ID, Student_ID, Transaction_Date, Description,
                    Transaction_Type, Amount, Credit, Debit, Balance
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (
                Transaction_ID.upper(), person.upper(), Transaction_Date, Reason.upper(), "CASH",
                Amount, False, True, endbalance
            ))
            connection.commit()
            print("Payment Success.")
            return True
            
    except Exception as e:
        print("An error occurred in Payment:", e)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Credit("730540_library_db", "Librarian", 100.00, "For new books")
# Debit("730540_library_db", "Librarian", "Kunal Das", 100.00, "For new books")

