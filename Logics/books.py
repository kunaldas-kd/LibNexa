import Logics.database_connector as database_connector 
import Logics.migrate_data as migrate_data 
# def insert_books(db_name, addbooks):
def insert_books(db_name, Book_Name, Author):
    connection = None
    cursor = None
    try:
        connection = database_connector.connect_to_db(db_name)
        if connection is None:
            print("Failed to connect to the database.")
            return
        
        cursor = connection.cursor()  
        # print(addbooks)
        # Book_ID = int(addbooks["id"])
        # Book_Name = addbooks["bookName"].upper()
        # Author = addbooks["author"].upper()

        cursor.execute('''SELECT Book_ID FROM books''')
        Books = cursor.fetchall()
        int_list = []
        skip_values = []

        for item in Books:
            try:
                int_list.append(int(item[0]))
            except ValueError:
                skip_values.append(item[0])  # Log non-integer Book_IDs

        # If there are valid integer IDs, get the max
        
        
       
        if not int_list:
            BookID = 1
            query = f"""
            SELECT QTY
            FROM book_stock
            WHERE Book_Name = %s AND Author = %s AND Is_BookID_Assigned = 'NO'
            """
            cursor.execute(query, (Book_Name, Author))
            Q = cursor.fetchone()
            print(Q[0])
            qty = Q[0]
            
            try:
                if qty < 1:
                        print("Quantity should be a positive integer.")
                        return
            except ValueError:
                print("Invalid quantity! It should be an integer.")
                return

                # Loop through the quantity and migrate data
            
            for _ in range(qty):  # Iterate 'qty' times
                migrate_data.migrate_data(cursor, connection, Book_Name, Author, str(BookID))
                BookID += 1
            print("Books successfully inserted into the database.")
            update_query = """
                UPDATE book_stock
                SET Is_BookID_Assigned = 'YES'
                WHERE Book_Name = %s AND Author = %s
            """
            cursor.execute(update_query, (Book_Name, Author))
            connection.commit()
            return True
            # else:
            #     return False

        
        else:
            Book_ID = max(int_list)
            BookID = int(Book_ID) + 1
            # print(BookID)
            query = f"""
            SELECT QTY
            FROM book_stock
            WHERE Book_Name = %s AND Author = %s AND Is_BookID_Assigned = 'NO'
            """
            cursor.execute(query, (Book_Name, Author))
            Q = cursor.fetchone()
            print(Q[0])
            qty = Q[0]
            
            try:
                if qty < 1:
                        print("Quantity should be a positive integer.")
                        return
            except ValueError:
                print("Invalid quantity! It should be an integer.")
                return

                # Loop through the quantity and migrate data
            
            for _ in range(qty):  # Iterate 'qty' times
                migrate_data.migrate_data(cursor, connection, Book_Name, Author, str(BookID))
                BookID += 1
            print("Books successfully inserted into the database.")
            update_query = """
                UPDATE book_stock
                SET Is_BookID_Assigned = 'YES'
                WHERE Book_Name = %s AND Author = %s
            """
            cursor.execute(update_query, (Book_Name, Author))
            connection.commit()
            return True
        # else:
        #     return False

    except Exception as e:
        print("An error occurred in books:", e)

    # finally:
    #     if cursor:
    #         cursor.close()
    #     if connection:
    #         connection.close()


# insert_books("_library_db")