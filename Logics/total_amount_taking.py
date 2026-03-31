import Logics.database_connector as database_connector
# import database_connector as database_connector
from datetime import datetime
def fatch_amount(USER, student):
    connection = None
    cursor = None
    
    try:
        connection = database_connector.connect_to_db(USER)
        if connection is None:
            print(f"Failed to connect to database: {USER}")
            return
        
        cursor = connection.cursor()
        query = """SELECT Return_Date FROM borrowed_books WHERE Student_ID = %s AND (Payment_Status = 'NOTHING TO PAY' OR Payment_Status = 'NOT PAID')"""
        cursor.execute(query, (student,))
        results = cursor.fetchall() # Fetch all matching rows
        query1 = """SELECT `Late Fine Amount` FROM users"""
        cursor.execute(query1)
        result1 = cursor.fetchall()
        
        perdayfine = float("{:.2f}".format(result1[0][0]))
        total_payable_amount = 0.00
        if not any(result for result in results):
            return total_payable_amount

        for result in results:
            fetched_return_date = result[0]  # Extract the Return_Date value from the result
            today = datetime.now().date()
            payable_amount = 0.00
            print(result1)    
            if today > fetched_return_date:
                overdue_minutes = (today - fetched_return_date).days  # Calculate overdue minutes
                payable_amount = overdue_minutes * perdayfine  # Assuming the fine is 1 unit per minute
                update_stock_status_query = """
                    UPDATE borrowed_books
                    SET Payable_Amount = %s,Payment_Status = 'NOT PAID'
                    WHERE Student_ID = %s AND Return_Date = %s AND (Payment_Status = 'NOTHING TO PAY' OR Payment_Status = 'NOT PAID')
                """
                cursor.execute(update_stock_status_query, (payable_amount,student,fetched_return_date))

                connection.commit()
                
            total_payable_amount += payable_amount

        total_payable_amount = float("{:.2f}".format(total_payable_amount))
        cursor.close()
        print(f"₹ {total_payable_amount}")
        return total_payable_amount
    except Exception as e:
        print("An error occurred in total_amount_taking:", e)
    
        
# take_amount("508435_library_db","D212206708")

def fatch_amount_1(USER, student):
    connection = None
    cursor = None
    
    try:
        connection = database_connector.connect_to_db(USER)
        cursor = connection.cursor()
        # connection = database_connector.connect_to_db(user_db_name)

        if connection:
            # cursor = connection.cursor()
            query = '''SELECT Submit FROM borrowed_books WHERE Student_ID = %s'''
            cursor.execute(query, (student,))
            results = cursor.fetchall()
            print(results)

            # Only proceed if student_id processing is fully complete
            if any(value[0] == 0 for value in results):
                return 0.00
            
            query = """SELECT Return_Date FROM borrowed_books WHERE Student_ID = %s AND (Payment_Status = 'NOTHING TO PAY' OR Payment_Status = 'NOT PAID')"""
            cursor.execute(query, (student,))
            results = cursor.fetchall() # Fetch all matching rows
            query1 = """SELECT `Late Fine Amount` FROM users"""
            cursor.execute(query1)
            result1 = cursor.fetchall()
            # print(result1)
            perdayfine = float("{:.2f}".format(result1[0][0]))
            total_payable_amount = 0
            if not any(result for result in results):
                return total_payable_amount

            for result in results:
                fetched_return_date = result[0]  # Extract the Return_Date value from the result
                today = datetime.now().date()
                payable_amount = 0.00
                
                if today > fetched_return_date:
                    overdue_minutes = (today - fetched_return_date).days  # Calculate overdue minutes
                    payable_amount = overdue_minutes * perdayfine  # Assuming the fine is 1 unit per minute
                    update_stock_status_query = """
                        UPDATE borrowed_books
                        SET Payable_Amount = %s,Payment_Status = 'NOT PAID'
                        WHERE Student_ID = %s AND Return_Date = %s AND (Payment_Status = 'NOTHING TO PAY' OR Payment_Status = 'NOT PAID')
                    """
                    cursor.execute(update_stock_status_query, (payable_amount,student,fetched_return_date))

                    connection.commit()
                    
                total_payable_amount += payable_amount

            total_payable_amount = float("{:.2f}".format(total_payable_amount))
            cursor.close()
            print(f"₹ {total_payable_amount}")
            return total_payable_amount
    except Exception as e:
        print("An error occurred in total_amount_taking:", e)


        


# take_amount("508435_library_db","D212206708")

def fatch_book_price(USER, bookid):
    connection = None
    cursor = None
    
    try:
        connection = database_connector.connect_to_db(USER)
        cursor = connection.cursor()
        # connection = database_connector.connect_to_db(user_db_name)

        if connection:
            # cursor = connection.cursor()
            query = '''SELECT Book_Price FROM books WHERE Book_ID = %s'''
            cursor.execute(query, (bookid,))
            results = cursor.fetchone()
            bookprice = results[0]
            return bookprice
            

            
    except Exception as e:
        print("An error occurred in total_amount_taking:", e)



# fatch_book_price("730540_library_db", 1000)