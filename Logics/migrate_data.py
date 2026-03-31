def migrate_data(cursor, connection, Book_Name, Author, BookID):
    # Stock_Status = "In Stock"
    source_query = f"""
    SELECT Book_Name, Author, Published_Year, Edition, Book_Price
    FROM book_stock
    WHERE Book_Name = %s AND Author = %s AND Is_BookID_Assigned = 'NO'
    """
    cursor.execute(source_query, (Book_Name, Author))
    rows = cursor.fetchall()

    if rows:
        insert_query = f"""
        INSERT INTO books (Book_ID, Book_Name, Author, Published_Year, Edition, Book_Price, Stock_Status) 
        VALUES (%s, %s, %s, %s, %s, %s, "In Stock")
        """
        for row in rows:
            cursor.execute(insert_query, (BookID, row[0], row[1], row[2], row[3], row[4]))

            connection.commit()
        print("Data migration complete!")
    else:
        print("No matching records found in book_stock")