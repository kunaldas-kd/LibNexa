# import Logics.database_connector as database_connector
import Logics.view_database as view_database
# import view_database
# import database_connector

def Payment_Function(conn, enable):
    
    try:
        # Convert to integer safely
        payment_enabled = int(enable)
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE users 
        SET 
            `Payment Functionality` = %s
    """, (payment_enabled,))
        conn.commit()

        return True

    except ValueError as ve:
        return {"status": "error", "message": f"Invalid input: {ve}"}

    except Exception as e:
        return {"status": "error", "message": f"Update failed: {str(e)}"}

def fetchstatus(conn):
    """
    Fetches the current payment functionality status.

    Returns:
        int (0 or 1) or dict with error message.
    """
    try:
        if conn is None:
            return {"status": "error", "message": "No DB connection."}

        cursor = conn.cursor()
        cursor.execute("""
            SELECT `Late Fine Amount`, `Borrowing Period`, Number_of_books, `Payment Functionality` 
            FROM users
        """)
        row = cursor.fetchone()
        if row is None:
            return {"status": "error", "message": "No user record found."}
        
        return row # Return only 'Payment Functionality'

    except Exception as e:
        return {"status": "error", "message": f"Fetch failed: {str(e)}"}


# def update_user_field(conn, field_name, value):
#     try:
#         if conn is None:
#             return {"status": "error", "message": "No database connection."}

#         cursor = conn.cursor()
#         query = f"UPDATE users SET `{field_name}` = %s"
#         cursor.execute(query, (value,))
#         conn.commit()
#         return True

#     except ValueError as ve:
#         return {"status": "error", "message": f"Invalid input: {ve}"}
#     except Exception as e:
#         return {"status": "error", "message": f"Failed to update {field_name}: {str(e)}"}
    
def run(conn, books, fine, period):
    
    if conn is None:
        print("❌ Database connection failed.")
        return
    
    view = view_database.view.user(conn)
    if not view or not view[0]:
        print("❌ No user data found.")
        conn.close()
        return

    user_data = view[0]

    # Safe conversion logic
    fine = float(fine) if fine not in (None, '', ' ') else float(user_data[4])
    period = period if period not in (None, '', ' ') else user_data[5]
    books = books if books not in (None, '', ' ') else user_data[6]
    if fine is None:
        res = fetchstatus(conn)
        print(res)
        if res[3] == 0:
            cursor = conn.cursor()
            query = "UPDATE users SET Number_of_books = %s, `Borrowing Period` = %s"
            cursor.execute(query, (books, period))
            conn.commit()
            return True
            
        else:
            cursor = conn.cursor()
            query = "UPDATE users SET Number_of_books = %s, `Late Fine Amount` = %s, `Borrowing Period` = %s"
            cursor.execute(query, (books, fine, period))
            conn.commit()
            return True
    else:
        res = fetchstatus(conn)
        print(res)
        if res[3] == 0:
            cursor = conn.cursor()
            query = "UPDATE users SET Number_of_books = %s, `Borrowing Period` = %s"
            cursor.execute(query, (books, period))
            conn.commit()
            return True
            
        else:
            cursor = conn.cursor()
            query = "UPDATE users SET Number_of_books = %s, `Late Fine Amount` = %s, `Borrowing Period` = %s"
            cursor.execute(query, (books, fine, period))
            conn.commit()
            return True
    
    # conn.close()



# user_db_name = f"{897738}_library_db"
# conn = database_connector.connect_to_db(user_db_name)
# run(conn, 4, 5, 30)
# fetchstatus(conn)