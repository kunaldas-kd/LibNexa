import Logics.database_connector as database_connector
# import database_connector
class view:
    @staticmethod
    def get_students(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        
        try:
            query ="SELECT * FROM students"  # Replace 'books' with your table name
            cursor.execute(query)
            studentlist = cursor.fetchall()
            cursor.close()
            # print(studentlist)
            return studentlist
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []
        
    @staticmethod
    def get_teachers(Id):
        try:
            conn = database_connector.connect_to_db(f"{Id}_library_db")
            if not conn:
                print("❌ Database connection failed.")
                return []

            with conn.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM teachers"
                cursor.execute(query)
                teacher_list = cursor.fetchall()
                cursor.close()
                return teacher_list

        except Exception as e:
            print(f"❌ Error fetching teacher list: {e}")
            return []



    @staticmethod
    def get_book_stock(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        
        try:
            query ="SELECT * FROM book_stock"  # Replace 'books' with your table name
            cursor.execute(query)
            bookstock = cursor.fetchall()
            cursor.close()
            return bookstock
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []
    @staticmethod
    def get_books(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        
        try:
            query ="SELECT * FROM books"  # Replace 'books' with your table name
            cursor.execute(query)
            books = cursor.fetchall()
            cursor.close()
            return books
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []

# view = ViewDatabase(connect_to_db("default_library_db"))  # Replace with your default DB name

                
    @staticmethod
    def get_borrowed_books(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        
        try:
            query ="SELECT * FROM borrowed_books"  # Replace 'books' with your table name
            cursor.execute(query)
            borrowed_books = cursor.fetchall()
            cursor.close()
            return borrowed_books
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []

# view.get_students("672554")

    @staticmethod
    def get_passedout_students(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        
        try:
            query = "SELECT * FROM Passedout_Students"
            cursor.execute(query)
            passedout_students = cursor.fetchall()
            cursor.close()
            return passedout_students
        except Exception as e:
            print(f"Error fetching passed-out students: {e}")
            return []
        
    @staticmethod    
    def get_cash_transactions(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        
        try:
            query = "SELECT * FROM cash_book"
            cursor.execute(query)
            transactions = cursor.fetchall()
            cursor.close()
            return transactions
        except Exception as e:
            print(f"Error fetching cash transactions: {e}")
            return []
    @staticmethod    
    def user(conn):
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM users"
            cursor.execute(query)
            transactions = cursor.fetchall()
            
            return transactions
        except Exception as e:
            print(f"Error fetching cash transactions: {e}")
            return []
        
    @staticmethod
    def get_teacher_borrowed_books(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Teacher_Borrowed_Books")
            borrowed_books = cursor.fetchall()
            return borrowed_books
        except Exception as e:
            print(f"Error fetching cash transactions: {e}")
            return []