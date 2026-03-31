import Logics.database_connector as database_connector

def get_book_details(book_id, db_name):
    """Fetches book details from the Books table based on Book_ID."""
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("Failed to connect to MySQL.")
        return None

    cursor = connection.cursor()
    try:
        query = """
            SELECT Book_ID, Book_Name, Author, Published_Year, Edition, Book_Price
            FROM Books
            WHERE Book_ID = %s
        """
        cursor.execute(query, (book_id,))
        result = cursor.fetchone()
        if result:
            book_details = {
                "Book_ID": result[0],
                "Book_Name": result[1],
                "Author": result[2],
                "Published_Year": result[3],
                "Edition": result[4],
                "Book_Price": result[5]
            }
            print(f"Book Details: {book_details}")
            return book_details
        else:
            print(f"No book found with Book_ID {book_id}.")
            return None
    except Exception as e:
        print(f"Error fetching book detail: {e}")
        return None
    # finally:
    #     cursor.close()
    #     connection.close()
