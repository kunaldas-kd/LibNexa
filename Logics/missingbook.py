import Logics.database_connector as database_connector
# import database_connector as database_connector

def missing_book(id,data):
    connection = None
    cursor = None
    try:
        # Connect to the database
        connection = database_connector.connect_to_db(id)
        if not connection:
            print("Database connection failed.")
            return False

        # Get Book ID input from user
        # missing_bookID = input_module.get_input("Enter the missing book ID: ")
        missing_bookID = data['bookID'].upper()
        reason = data['reason'].upper()

        if not missing_bookID:
            print("Invalid Book ID.")
            return False

        cursor = connection.cursor()

        # Get book details
        book_query = '''
        SELECT Book_Name, Author, Published_Year, Edition, Stock_Status
        FROM books
        WHERE Book_ID = %s
        '''
        cursor.execute(book_query, (missing_bookID,))
        book_row = cursor.fetchone()

        if not book_row:
            print("Book details not found.")
            return False

        Book_Name, Author, Published_Year, Edition, Stock_Status = book_row

        if Stock_Status in ['Out of Stock', 'In Stock']:
            # Update book status to "BOOK MISSING"
            update_book_query = '''
            UPDATE books
            SET Stock_Status = %s
            WHERE Book_ID = %s
            '''
            cursor.execute(update_book_query, (reason, missing_bookID,))
            connection.commit()
            print("Book status updated successfully in 'books' table.")

            # Get current stock quantity
            stock_query = '''
            SELECT QTY
            FROM book_stock
            WHERE Book_Name = %s AND Author = %s AND Published_Year = %s AND Edition = %s
            '''
            cursor.execute(stock_query, (Book_Name, Author, Published_Year, Edition))
            stock_row = cursor.fetchone()

            if not stock_row:
                print("Book stock details not found.")
                return False

            qty = stock_row[0]
            new_qty = max(qty - 1, 0)

            # Update stock quantity
            update_stock_query = '''
            UPDATE book_stock
            SET QTY = %s
            WHERE Book_Name = %s AND Author = %s AND Published_Year = %s AND Edition = %s
            '''
            cursor.execute(update_stock_query, (new_qty, Book_Name, Author, Published_Year, Edition))
            connection.commit()
            print("Stock quantity updated successfully.")

            return True
        else:
            print("Book is already marked as missing or unavailable for status update.")
            return False

    # except Exception as e:
    #     print(f"[Error] {e}")
    #     return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# missing_book("508435_library_db")

def bookcalculation(id):
    connection = None
    cursor = None
    try:
        # Connect to the database
        connection = database_connector.connect_to_db(f"{id}_library_db")
        if not connection:
            print("Database connection failed.")
            return False

        cursor = connection.cursor()
        book_query = '''
        SELECT QTY
        FROM book_stock
        '''
        cursor.execute(book_query)
        books = cursor.fetchall()
        inbook_query = '''
        SELECT COUNT(Stock_Status)
        FROM books WHERE Stock_Status = 'In Stock'
        '''
        cursor.execute(inbook_query)
        inbooks = cursor.fetchall()
        outbook_query = '''
        SELECT COUNT(Stock_Status)
        FROM books WHERE Stock_Status = 'Out of Stock'
        '''
        cursor.execute(outbook_query)
        outbooks = cursor.fetchall()

        missing_book_query = '''
            SELECT COUNT(Stock_Status)
            FROM books
            WHERE Stock_Status NOT IN ('Out of Stock', 'In Stock')
        '''
        cursor.execute(missing_book_query)
        missingbooks = cursor.fetchall()
        # Extract and sum quantities
        total_Instock = sum(qty[0] for qty in inbooks)
        # print(f"Total book quantity: {total_Instock}")
        total_outofstock = sum(qty[0] for qty in outbooks)
        # print(f"Total book quantity: {total_outofstock}")
        total_qty = sum(qty[0] for qty in books)
        total_missingbooks = sum(qty[0] for qty in missingbooks)
        print(f"Total book quantity: {total_missingbooks}")
        return total_qty, total_Instock, total_outofstock, total_missingbooks

    except Exception as e:
        print(f"[Error] {e}")
        return False

# bookcalculation1("949028")

def Total_student(id):
    connection = None
    cursor = None
    try:
        # Connect to the database
        connection = database_connector.connect_to_db(f"{id}_library_db")
        if not connection:
            print("Database connection failed.")
            return False

        cursor = connection.cursor()
        student_query = '''
        SELECT COUNT(Student_ID)
        FROM students
        '''
        cursor.execute(student_query)
        totalstudent = cursor.fetchall()

        # Extract and sum quantities
        total_qty = sum(qty[0] for qty in totalstudent)
        print(f"Total book quantity: {total_qty}")
        return total_qty

    except Exception as e:
        print(f"[Error] {e}")
        return False

# Total_student("949028_library_db")



def Total_Issued(id):
    connection = None
    cursor = None
    try:
        # Connect to the database
        connection = database_connector.connect_to_db(f"{id}_library_db")
        if not connection:
            print("Database connection failed.")
            return False

        cursor = connection.cursor()
        Borrow_query = '''
        SELECT COUNT(*)
        FROM borrowed_books
        '''
        cursor.execute(Borrow_query)
        total = cursor.fetchall()

        Borrow_query = '''
        SELECT COUNT(Borrow)
        FROM borrowed_books WHERE Borrow = '1'
        '''
        cursor.execute(Borrow_query)
        Borrow = cursor.fetchall()

        submit_query = '''
        SELECT COUNT(Submit)
        FROM borrowed_books WHERE Submit = '1'
        '''
        cursor.execute(submit_query)
        submit = cursor.fetchall()

        Renew_query = '''
        SELECT COUNT(Renew)
        FROM borrowed_books WHERE Renew = '1'
        '''
        cursor.execute(Renew_query)
        Renew = cursor.fetchall()

        # returndate_query = '''
        # SELECT Return_Date
        # FROM borrowed_books
        # '''
        # cursor.execute(returndate_query)
        # returndate = cursor.fetchall()
        # print(returndate)
        
        # Extract and sum quantities
        Total = sum(qty[0] for qty in total)
        print(f"Total borrowed: {Total}")
        issued = sum(qty[0] for qty in Borrow)
        print(f"Total borrowed: {issued}")
        Submit = sum(qty[0] for qty in submit)
        print(f"Total borrowed: {Submit}")
        renew = sum(qty[0] for qty in Renew)
        print(f"Total borrowed: {renew}")
        return issued, total,  Submit, renew

    except Exception as e:
        print(f"[Error] {e}")
        return False

# Total_Issued(949028)
# Total_Issued(163452)

def Total_teacher(id):
    connection = None
    cursor = None
    try:
        connection = database_connector.connect_to_db(f"{id}_library_db")
        if not connection:
            print("❌ Database connection failed.")
            return False

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM teachers")
        result = cursor.fetchall()

        total_teachers = sum(qty[0] for qty in result)
        print(f"👨‍🏫 Total teacher count: {total_teachers}")
        return total_teachers

    except Exception as e:
        print(f"❌ Error in Total_teacher(): {e}")
        return False
    
# Total_teacher(204712)


def Total_Teacher_Issued(id):
    connection = None
    cursor = None
    try:
        # Connect to the database
        connection = database_connector.connect_to_db(f"{id}_library_db")
        if not connection:
            print("Database connection failed.")
            return False

        cursor = connection.cursor()

        # Total issued records
        cursor.execute("SELECT COUNT(*) FROM teacher_borrowed_books")
        total = cursor.fetchone()[0]

        # Currently borrowed (Borrow = 1)
        cursor.execute("SELECT COUNT(*) FROM teacher_borrowed_books WHERE Borrow = '1'")
        issued = cursor.fetchone()[0]

        # Total submitted (Submit = 1)
        cursor.execute("SELECT COUNT(*) FROM teacher_borrowed_books WHERE Submit = '1'")
        submitted = cursor.fetchone()[0]

        print(f"📚 Total records in borrowed_books: {total}")
        print(f"✅ Currently borrowed (Borrow=1): {issued}")
        print(f"📥 Total submitted (Submit=1): {submitted}")

        return issued, total,  submitted

    except Exception as e:
        print(f"[Error] {e}")
        return False