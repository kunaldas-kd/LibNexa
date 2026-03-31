import Logics.database_connector as database_connector
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_user_database(Id):
    """Creates a new database for the user."""
    connection = database_connector.connect_to_db()
    if connection is None:
        logging.error("Failed to connect to MySQL.")
        return

    cursor = connection.cursor()
    try:
        db_name = f"{Id}_library_db"
        cursor.execute(f"CREATE DATABASE `{db_name}`")
        logging.info(f"Database `{db_name}` created successfully.")
        setup_library_tables(db_name)
    except Exception as e:
        logging.error(f"Error creating database: {e}")
    finally:
        cursor.close()
        connection.close()

def setup_library_tables(db_name):
    """Creates the required tables for a library database."""
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        logging.error(f"Failed to connect to `{db_name}`.")
        return

    try:
        create_users_table(connection)
        create_book_stock_table(connection)
        create_books_table(connection)
        create_students_table(connection)
        create_borrowed_books_table(connection)
        create_cash_book_table(connection)
        create_passedout_students_table(connection)
        create_cash_book_table(connection)
        create_teachers_table(connection)
        create_teacher_borrowed_books_table(connection)
            
        logging.info(f"Tables created successfully in `{db_name}`.")
    except Exception as e:
        logging.error(f"Error creating tables in database setup: {e}")
    finally:
        connection.close()

def create_users_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                Id VARCHAR(50) PRIMARY KEY,
                Library_name VARCHAR(50) NOT NULL,
                Institute_name VARCHAR(50) NOT NULL,
                Institute_Email VARCHAR(50) NOT NULL,
                Address VARCHAR(50) NOT NULL,
                District VARCHAR(50) NOT NULL,
                State VARCHAR(50) NOT NULL,
                Country VARCHAR(50) NOT NULL,
                `Late Fine Amount` INT NOT NULL,
                Passwords VARCHAR(50) NOT NULL,
                `Borrowing Period` INT NOT NULL,
                Number_of_books INT NOT NULL,
                `MAC Address` VARCHAR(255),
                `Payment Functionality` INT NOT NULL
            )
        """)
        logging.info("Users table created successfully.")
    except Exception as e:
        logging.error(f"Error creating Users table: {e}")
    finally:
        cursor.close()

def create_book_stock_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Book_Stock (
                SL_No INT AUTO_INCREMENT PRIMARY KEY,
                Book_Name VARCHAR(255) NOT NULL,
                Author VARCHAR(255) NOT NULL,
                Edition VARCHAR(50) NOT NULL,
                Publisher VARCHAR(255) NOT NULL,
                Place_of_Publication VARCHAR(255) NOT NULL,
                Published_Year INT,
                QTY INT,
                Book_Price INT,
                Order_Challan_Bill_Info VARCHAR(255) NOT NULL,
                Source VARCHAR(255) NOT NULL,
                Stock_Date DATE NOT NULL,
                Stock_Time TIME NOT NULL,
                Is_BookID_Assigned VARCHAR(255) NOT NULL
            );
        """)
        # UNIQUE (Book_Name, Author, Published_Year, Edition, Book_Price),
        logging.info("Book_Stock table created successfully.")
    except Exception as e:
        logging.error(f"Error creating Book_Stock table: {e}")
    finally:
        cursor.close()

def create_books_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Books (
                Book_ID VARCHAR(255) PRIMARY KEY,
                Book_Name VARCHAR(255) NOT NULL,
                Author VARCHAR(255) NOT NULL,
                Published_Year INT,
                Edition VARCHAR(50) NOT NULL,
                Book_Price INT,
                Stock_Status VARCHAR(50) NOT NULL
            );
        """)
        logging.info("Books table created successfully.")
    except Exception as e:
        logging.error(f"Error creating Books table: {e}")
    finally:
        cursor.close()

def create_students_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                Student_ID VARCHAR(50) PRIMARY KEY,
                Student_Name VARCHAR(50) NOT NULL,
                Date_Of_Birth DATE NOT NULL,
                Department VARCHAR(50) NOT NULL,
                Student_Email VARCHAR(50) NOT NULL,
                Phone_Number VARCHAR(15) NOT NULL,
                Address VARCHAR(255) NOT NULL,
                Admission_Year VARCHAR(10) NOT NULL
            )
        """)
        logging.info("Students table created successfully.")
    except Exception as e:
        logging.error(f"Error creating Students table: {e}")
    finally:
        cursor.close()

def create_borrowed_books_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Borrowed_Books (
                Sl_No INT AUTO_INCREMENT PRIMARY KEY,
                Book_ID VARCHAR(255) NOT NULL,
                Student_ID VARCHAR(50) NOT NULL,
                Student_Name VARCHAR(50) NOT NULL,
                Student_Email VARCHAR(50) NOT NULL,
                Department VARCHAR(50) NOT NULL,
                Book_Name VARCHAR(255) NOT NULL,
                Author VARCHAR(255) NOT NULL,
                Published_Year INT,
                Edition VARCHAR(50) NOT NULL,
                Book_Price INT,
                Borrow_Date DATE NOT NULL,
                Return_Date DATE NOT NULL,
                Payable_Amount DECIMAL(10, 2) NOT NULL,
                Borrow BOOLEAN DEFAULT FALSE,
                Submit BOOLEAN DEFAULT FALSE,
                Renew BOOLEAN DEFAULT FALSE,
                Payment_Status VARCHAR(50) NOT NULL,
                Reminder VARCHAR(50) NOT NULL
            );
        """)
        logging.info("Borrowed_Books table created successfully.")
    except Exception as e:
        logging.error(f"Error creating Borrowed_Books table: {e}")
    finally:
        cursor.close()

def create_passedout_students_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Passedout_Students (
                SL_No INT AUTO_INCREMENT PRIMARY KEY,
                Student_ID VARCHAR(50) UNIQUE NOT NULL,
                Student_Name VARCHAR(255) NOT NULL,
                Certificate_No VARCHAR(100) NOT NULL,
                Department VARCHAR(100) NOT NULL,
                Student_Email VARCHAR(255) NOT NULL,
                Phone_Number VARCHAR(15) NOT NULL,
                Passedout_Year INT NOT NULL,
                Certificate LONGBLOB
            );
        """)
        logging.info("Students table created successfully.")
    except Exception as e:
        logging.error(f"Error creating Students table: {e}")
    finally:
        cursor.close()


def create_cash_book_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cash_book (
                Sl_No INT AUTO_INCREMENT PRIMARY KEY,
                Transaction_Id VARCHAR(50) UNIQUE,
                Student_Id VARCHAR(50) NOT NULL,
                Transaction_Date VARCHAR(50) NOT NULL,
                Description VARCHAR(255),
                Transaction_Type VARCHAR(255) NOT NULL,
                Amount VARCHAR(50) NOT NULL,
                Credit VARCHAR(50) NOT NULL,
                Debit VARCHAR(50) NOT NULL,
                Balance DECIMAL(10, 2) NOT NULL
            );
        """)
        logging.info("cash_book table created successfully.")
    except Exception as e:
        logging.error(f"Error creating cash_book table: {e}")
    finally:
        cursor.close()




def create_teachers_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Teachers (
                Teacher_ID VARCHAR(50) PRIMARY KEY,
                Teacher_Name VARCHAR(50) NOT NULL,
                Designation VARCHAR(50) NOT NULL,
                Department VARCHAR(50) NOT NULL,
                Teacher_Email VARCHAR(50) NOT NULL,
                Phone_Number VARCHAR(15) NOT NULL,
                Address VARCHAR(255) NOT NULL,
                Joining_Year VARCHAR(10) NOT NULL,
                Employment_Status VARCHAR(15) NOT NULL
            )
        """)
        logging.info("✅ Teachers table created successfully.")
    except Exception as e:
        logging.error(f"❌ Error creating Teachers table: {e}")
    finally:
        cursor.close()

def create_teacher_borrowed_books_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Teacher_Borrowed_Books (
                    Sl_No INT AUTO_INCREMENT PRIMARY KEY,
                    Book_ID VARCHAR(255) NOT NULL,
                    Teacher_ID VARCHAR(50) NOT NULL,
                    Teacher_Name VARCHAR(50) NOT NULL,
                    Department VARCHAR(50) NOT NULL,
                    Book_Name VARCHAR(255) NOT NULL,
                    Author VARCHAR(255) NOT NULL,
                    Published_Year INT NOT NULL,
                    Edition VARCHAR(50) NOT NULL,
                    Book_Price INT NOT NULL,
                    Borrow_Date DATE NOT NULL,
                    Borrow BOOLEAN NOT NULL,
                    Submit BOOLEAN NOT NULL
                );
        """)
        logging.info("Borrowed_Books table created successfully.")
    except Exception as e:
        logging.error(f"Error creating Borrowed_Books table: {e}")
    finally:
        cursor.close()




def setup_admin_interface_database():
    """Creates the Admin_Interface database if it does not exist."""
    connection = database_connector.connect_to_db()
    if connection is None:
        logging.error("❌ Failed to connect to MySQL server.")
        return

    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS Admin_Interface")
        logging.info("✅ Admin_Interface database created or already exists.")
        setup_id_pass_table()
    except Exception as e:
        logging.error(f"❌ Error creating Admin_Interface database: {e}")
    finally:
        cursor.close()
        connection.close()

def setup_id_pass_table():
    """Creates the id_pass table inside Admin_Interface database."""
    connection = database_connector.connect_to_db("Admin_Interface")
    if connection is None:
        logging.error("❌ Failed to connect to Admin_Interface database.")
        return

    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS id_pass (
                Id VARCHAR(50) PRIMARY KEY,
                Library_name VARCHAR(50) NOT NULL,
                Institute_name VARCHAR(50) NOT NULL,
                Institute_Email VARCHAR(50) NOT NULL,
                Address VARCHAR(50) NOT NULL,
                District VARCHAR(50) NOT NULL,
                State VARCHAR(50) NOT NULL,
                Country VARCHAR(50) NOT NULL,
                `Late Fine Amount` INT NOT NULL,
                Passwords VARCHAR(50) NOT NULL,
                `Borrowing Period` INT NOT NULL,
                Number_of_books INT NOT NULL,
                date DATE NOT NULL,
                time TIME NOT NULL
            );
        """)
        logging.info("✅ id_pass table created successfully in Admin_Interface.")
    except Exception as e:
        logging.error(f"❌ Error creating id_pass table: {e}")
    finally:
        cursor.close()
        connection.close()