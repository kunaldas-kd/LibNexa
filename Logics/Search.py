import Logics.database_connector as database_connector
import tabulate
import Logics.input_module as input_module
def search_books(db_name):
    """Prompts user for input and searches for books in the database."""
    while True:
        search = input_module.get_input("Enter search criteria \n1. BOOK ID \n2. BOOK NAME \n3. AUTHOR \n4. PUBLISHED YEAR \n5. BACK : ")
        if search == '1':
            book_id = input("Book ID: ")
            search_books1(db_name, book_id=book_id)
            break
        elif search == '2':
            book_name = input("Book Name: ")
            search_books1(db_name, book_name=book_name)
            break
        elif search == '3':
            author = input("Author: ")
            search_books1(db_name, author=author)
            break
        elif search == '4':
            published_year = input("Published Year: ")
            search_books1(db_name, published_year=published_year)
            break
        elif search == '5':
            break
        else:
            print("Invalid Choice. Please enter 1, 2, 3, or 4.")
def search_bookSTOCK(db_name):
    """Prompts user for input and searches for books in the database."""
    while True:
        search = input_module.get_input("Enter search criteria \n1. BOOK NAME \n2. AUTHOR \n3. PUBLISHED YEAR \n4. BACK : ")
        if search == '1':
            book_name = input("Book Name: ")
            search_books2(db_name, book_name=book_name)
            break
        elif search == '2':
            author = input("Author: ")
            search_books2(db_name, author=author)
            break
        elif search == '3':
            published_year = input("Published Year: ")
            search_books2(db_name, published_year=published_year)
            break
        elif search == '4':
            break
        else:
            print("Invalid Choice. Please enter 1, 2 or 3.")
    # Convert empty inputs to None
    # book_id = int(book_id) if book_id else None
    # published_year = int(published_year) if published_year else None
    # book_name = book_name if book_name else None
    # author = author if author else None
def search_books1(db_name, book_id=None, book_name=None, published_year=None, author=None):
    book_id = int(book_id) if book_id else None
    published_year = int(published_year) if published_year else None
    book_name = book_name if book_name else None
    author = author if author else None
    try:
        # Connect to the database
        connection = database_connector.connect_to_db(db_name)
        if not connection:
            return
        
        cursor = connection.cursor()

        # SQL query
        query = """
        SELECT * FROM books
        WHERE (%s IS NULL OR Book_ID = %s)
        AND (%s IS NULL OR LOWER(Book_Name) = LOWER(%s))
        AND (%s IS NULL OR LOWER(Author) = LOWER(%s))
        AND (%s IS NULL OR Published_Year = %s)
        """
        parameters = (book_id, book_id, book_name, book_name, author, author, published_year, published_year)

        # Execute query
        cursor.execute(query, parameters)
        results = cursor.fetchall()
        while True:
            # Display results
            if results:
                headers = [i[0] for i in cursor.description]  # Get column names
                print("\nSearch Results:")
                print(tabulate.tabulate(results, headers=headers, tablefmt="grid"))
                r = input_module.get_input("\nEnter b to back: ")
                if r == "b" or "B":
                    break
                else:
                    print("\nInvalid Choice.\n")
            else:
                print("\nNo matching books found.\n")
                r = input_module.get_input("\nEnter b to back: ")
                if r == "b" or "B":
                    break
                else:
                    print("Invalid Choice.")

        # Close connection
        connection.close()
    except Exception as e:
        print(f"Search Error: {e}")
    
    finally:
        cursor.close()
        connection.close()


def search_books2(db_name, book_name=None, published_year=None, author=None):
    published_year = int(published_year) if published_year else None
    book_name = book_name if book_name else None
    author = author if author else None
    try:
        # Connect to the database
        connection = database_connector.connect_to_db(db_name)
        if not connection:
            return
        
        cursor = connection.cursor()

        # SQL query
        query = """
        SELECT * FROM book_stock
        WHERE (%s IS NULL OR LOWER(Book_Name) = LOWER(%s))
        AND (%s IS NULL OR LOWER(Author) = LOWER(%s))
        AND (%s IS NULL OR Published_Year = %s)
        """
        parameters = (book_name, book_name, author, author, published_year, published_year)

        # Execute query
        cursor.execute(query, parameters)
        results = cursor.fetchall()
        while True:
            # Display results
            if results:
                headers = [i[0] for i in cursor.description]  # Get column names
                print("\nSearch Results:")
                print(tabulate.tabulate(results, headers=headers, tablefmt="grid"))
                r = input_module.get_input("\nEnter b to back: ")
                if r == "b" or "B":
                    break
                else:
                    print("\nInvalid Choice.\n")
            else:
                print("\nNo matching books found.\n")
                r = input_module.get_input("\nEnter b to back: ")
                if r == "b" or "B":
                    break
                else:
                    print("Invalid Choice.")

        # Close connection
        connection.close()
    except Exception as e:
        print(f"Search Error: {e}")
    
    finally:
        cursor.close()
        connection.close()