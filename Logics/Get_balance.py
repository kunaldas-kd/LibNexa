import Logics.database_connector as database_connector
# import database_connector as database_connector
def credit(Id):
    try:
        # conn = database_connector.connect_to_db(f"{Id}_library_db")
        conn = database_connector.connect_to_db(Id)
        cursor = conn.cursor()

        query = """
        SELECT Balance FROM cash_book
        ORDER BY Sl_No DESC
        LIMIT 1;
        """

        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            print("Last Amount:", result[0])
            return result[0]
        else:
            print(0)
            return 0

    except Exception as e:
        print("Error occurred in Credit:", e)

    # finally:   
    #     cursor.close()
    #     conn.close() 

# credit(730540)