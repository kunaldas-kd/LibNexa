import random
import datetime
import Logics.database_connector as database_connector 
import Logics.database_setup as database_setup 
import Logics.password_generator as password_generator 
import Logics.send_email as send_email
import Logics.Excel_Templates as Excel_Templates
import backup
def copy_credentials(Id):
    connection = None
    cursor = None
    try:
        # Connect to Admin_Interface database
        connection = database_connector.connect_to_db('Admin_Interface')
        if connection is None:
            print("Failed to connect to Admin_Interface database.")
            return
        cursor = connection.cursor()
        
        # Retrieve user ID and password from Admin_Interface database
        cursor.execute("SELECT Id, Library_name, Institute_name, Institute_Email, Address, District, State, Country, Passwords, `Late Fine Amount`, `Borrowing Period`, Number_of_books FROM id_pass WHERE Id = %s", (Id,))
        credentials = cursor.fetchone()
        if credentials:
            Id, Library_name, Institute_name, Institute_Email, Address, District, State, Country, Passwords, latefine, borrowing_period, AlottedBooks = credentials

            # Connect to user-specific database
            user_db_name = f"{Id}_library_db"
            connection = database_connector.connect_to_db(user_db_name)
            if connection is None:
                print(f"Failed to connect to {user_db_name} database.")
                return
            cursor = connection.cursor()

            # Insert user ID and password into user-specific database
            cursor.execute("INSERT INTO Users (Id, Library_name, Institute_name, Institute_Email, Address, District, State, Country, Passwords, `Late Fine Amount`, `Borrowing Period`, Number_of_books, `Payment Functionality`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (Id, Library_name, Institute_name, Institute_Email, Address, District, State, Country, Passwords, latefine, borrowing_period, AlottedBooks, "1",))
            connection.commit()
            print(f"Credentials copied successfully to {user_db_name}.")
        else:
            print(f"No credentials found for user ID: {Id}")

    except Exception as e:
        print(f"Error copying credentials in library_info(insert_library_info): {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



def insert_library_info(data):
    """Inserts library information when the user registers and returns the generated user_id."""
    connection = None
    cursor = None
    try:
        connection = database_connector.connect_to_db('Admin_Interface')
        if connection is None:
            print("Failed to connect to the database.")
            return None

        cursor = connection.cursor()
                
        # For Frontend interface 
        Id = random.randint(100000, 999999)
        Library_name = data["libraryName"].upper()
        Institute_name = data["instituteName"].upper()
        Institute_Email = data["instituteEmail"].upper()
        # validation.Valid.verify_email(Institute_Email)
        # EMAIL_EXISTANCE.validate_email(Institute_Email)
        Address = data["address"].upper()
        District = data["district"].upper()
        State = data["state"].upper()
        Country = data["country"].upper()
        latefine = float(data["latefine"])
        borrowing_period = int(data["borrowingPeriod"])
        
        AlottedBooks = int(data["AlottedBooks"])
        Passwords = password_generator.generate_password()
        date = datetime.date.today()
        time = datetime.datetime.now().time()
        

        
        insert_query = """
        INSERT INTO id_pass (Id, Library_name, Institute_name, Institute_Email, Address, District, State, Country, Passwords, `Late Fine Amount`, date, time, `Borrowing Period`, Number_of_books)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (Id, Library_name, Institute_name, Institute_Email, Address, District, State, Country, Passwords, latefine, date, time, borrowing_period, AlottedBooks))
        connection.commit()
        print("Data insertion complete!")
        
        send_email.send_email(Institute_Email, Id, Passwords, Library_name)
        database_setup.create_user_database(Id)
        copy_credentials(Id)
        backup.backuploop(Id)
        Excel_Templates.Excel()
        print("done")
        return True
    
    # except Exception as e:
    #     print("An error occurred in library_info(insert_library_info):", e)
    #     return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()





