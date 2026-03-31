# import database_connector
import Logics.database_connector as database_connector
import datetime
def getbookdetails(Id, bookID):
    connection = None
    cursor = None
    try:
        connection = database_connector.connect_to_db(Id)
        if not connection:
            return False
        
        else:
            cursor = connection.cursor()
            book_query = '''
            SELECT Book_Name, Author, Published_Year, Edition, Book_Price FROM books WHERE Book_ID = %s
            '''
            cursor.execute(book_query, (bookID,))
            book_row = cursor.fetchone()

            bookname, author, Published_Year, Edition, Price = book_row
            
            if not book_row:
                print("Book details not found.")
                return False
            else:
                print(f"{bookname} by {author}")
                return {"bookname": bookname, "author": author,"Published_Year": Published_Year, "Edition": Edition, "Price": Price}
    except Exception as e:
        print(f"[Error] {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# getbookdetails("730540_library_db", 1000)



def Confirm_Book(Id, bookID, publishedYear , edition, bookPrice):
    connection = None
    cursor = None
    try:
        connection = database_connector.connect_to_db(Id)
        if not connection:
            return False

        cursor = connection.cursor()

        # Get existing Edition
        cursor.execute("SELECT Published_Year, Edition, Book_Price FROM books WHERE Book_ID = %s", (bookID,))
        book_row = cursor.fetchone()

        if not book_row:
            print("Book details not found.")
            return False

        PublishedYear, Edition, Price = book_row

        if int(publishedYear) != int(PublishedYear) or edition.strip().upper() != Edition.strip().upper() or float(Price) != float(bookPrice):
            # Update Edition and Price
            cursor.execute("""
                UPDATE books SET Published_Year = %s, Edition = %s, Book_Price = %s, Stock_Status = 'In Stock' WHERE Book_ID = %s
            """, (publishedYear, edition.upper(), bookPrice, bookID))
            connection.commit()
            print("Book status updated successfully in 'books' table.")


            return True
        else:
            print("Edition matches existing record. No update needed.")
            return False

    except Exception as e:
        print(f"[Error] {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()