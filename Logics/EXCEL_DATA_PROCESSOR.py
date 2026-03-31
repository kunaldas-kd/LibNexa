import os
import pandas as pd
from datetime import datetime
import mysql.connector
import Logics.database_connector as database_connector
from datetime import datetime, time, date

class UniversalProcessor:

    @staticmethod
    def read_excel(file_path):
        try:
            df = pd.read_excel(file_path)
            if df.empty:
                print(f"[SKIPPED] Empty file: {file_path}")
                return None
            print(f"[INFO] Columns in file: {df.columns.tolist()}")
            return df
        except Exception as e:
            print(f"[ERROR] Reading Excel: {e}")
            return None

    @staticmethod
    def detect_table_from_df(df):
        # Normalize column names: lowercase and strip whitespace
        original_columns = df.columns.tolist()
        columns = set(col.strip().lower() for col in original_columns)

        # print(f"[DEBUG] Original columns detected: {original_columns}")
        # print(f"[DEBUG] Normalized columns detected: {columns}")

        if {"book_id", "book_name", "author", "published_year", "edition", "book_price", "stock_status"}.issubset(columns):
            return "books"

        elif {"sl_no", "book_name", "author", "edition", "publisher", "place_of_publication",
            "published_year", "qty", "book_price", "order_challan_bill_info", "source",
            "stock_date", "stock_time", "is_bookid_assigned"}.issubset(columns):
            return "book_stock"

        elif {"student_id", "student_name", "date_of_birth", "department", "student_email", 
            "phone_number", "address", "admission_year"}.issubset(columns):
            return "students"

        elif {"teacher_id", "teacher_name", "designation", "department",
            "teacher_email", "phone_number", "address", "joining_year", "employment_status"}.issubset(columns):
            return "teachers"

        elif {"sl_no", "transaction_id", "student_id", "transaction_date",
            "description", "transaction_type", "amount", "credit", "debit", "balance"}.issubset(columns):
            return "cash_book"

        elif {"sl_no", "student_id", "student_name", "certificate_no", "department",
            "student_email", "phone_number", "passedout_year", "certificate"}.issubset(columns):
            return "passedout_students"

        elif {"sl_no", "book_id", "student_id", "student_name", "student_email", "department",
                "book_name", "author", "published_year", "edition", "book_price", "borrow_date", 
                "return_date", "payable_amount", "borrow", "submit", "renew", "payment_status", "reminder"
                }.issubset(columns):
            return "borrowed_books"

        elif {"sl_no", "book_id", "teacher_id", "teacher_name", "department",
            "book_name", "author", "published_year", "edition",
            "book_price", "borrow_date", "borrow", "submit"}.issubset(columns):
            return "teacher_borrowed_books"

        else:
            return None

    @staticmethod
    def parse_date_safe(value):
        if isinstance(value, datetime):
            return value.date()
        elif isinstance(value, str):
            for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
                try:
                    return datetime.strptime(value, fmt).date()
                except:
                    continue
        return None

    @staticmethod
    def validate_required_fields(row, required_fields):
        for field in required_fields:
            if pd.isna(row.get(field)) or row.get(field) == "":
                # print(f"[SKIPPED] Missing required field: {field} in row: {row.to_dict()}")
                return False
        return True

    # ============================= INSERT FUNCTIONS =============================

    @staticmethod
    def insert_books(df, conn):
        with conn.cursor() as cursor:
            for _, row in df.iterrows():
                try:
                    if not UniversalProcessor.validate_required_fields(row, ['Book_ID']):
                        continue
                    cursor.execute("""
                        INSERT INTO books 
                        (Book_ID, Book_Name, Author, Published_Year, Edition, Book_Price, Stock_Status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        str(row.get('Book_ID', '')).upper(),
                        str(row.get('Book_Name', '')).upper(),
                        str(row.get('Author', '')).upper(),
                        str(row.get('Published_Year', '')) if row.get('Published_Year') else None,
                        str(row.get('Edition', '')).upper(),
                        str(row.get('Book_Price', 0)),
                        str(row.get('Stock_Status', ''))
                    ))
                except mysql.connector.Error as e:
                    # print(f"[ERROR] insert_books row failed: {e} | Row: {row.to_dict()}")
                    continue
        print("[INFO] Inserted into books")

    @staticmethod
    def insert_book_stock(df, conn):
        with conn.cursor() as cursor:
            for _, row in df.iterrows():
                try:
                    # Convert 'Stock_Date' safely
                    stock_date = UniversalProcessor.parse_date_safe(row.get('Stock_Date'))
                    
                    # Convert 'Stock_Time' (float from Excel) to time object
                    stock_time_val = row.get('Stock_Time')
                    if isinstance(stock_time_val, float):
                        # Convert Excel float time to Python time
                        total_seconds = int(stock_time_val * 24 * 3600)
                        hours = total_seconds // 3600
                        minutes = (total_seconds % 3600) // 60
                        seconds = total_seconds % 60
                        stock_time = time(hour=hours, minute=minutes, second=seconds)
                    else:
                        stock_time = None
                    cursor.execute("""
                        INSERT IGNORE INTO book_stock 
                        (SL_No, Book_Name, Author, Published_Year, Edition, Publisher, Place_of_Publication, 
                         QTY, Book_Price, Order_Challan_Bill_Info, Source, Stock_Date, Stock_Time, Is_BookID_Assigned)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        int(row.get('SL_No', 0)),
                        str(row.get('Book_Name', '')).upper(),
                        str(row.get('Author', '')).upper(),
                        row.get('Published_Year', 0),
                        str(row.get('Edition', '')).upper(),
                        str(row.get('Publisher', '')).upper(),
                        str(row.get('Place_of_Publication', '')).upper(),
                        int(row.get('QTY', 0)),
                        float(row.get('Book_Price', 0)),
                        str(row.get('Order_Challan_Bill_Info', '')).upper(),
                        str(row.get('Source', '')).upper(),
                        stock_date,
                        stock_time,
                        str(row.get('Is_BookID_Assigned', '')).upper()
                    ))
                except mysql.connector.Error as e:
                    # print(f"[ERROR] insert_book_stock row failed: {e} | Row: {row.to_dict()}")
                    continue
        print("[INFO] Inserted into book_stock")

    @staticmethod
    def insert_students(df, conn):
        with conn.cursor() as cursor:
            for _, row in df.iterrows():
                try:
                    if not UniversalProcessor.validate_required_fields(row, ['Student_ID', 'Student_Name', 'Date_Of_Birth']):
                        continue
                    dob = UniversalProcessor.parse_date_safe(row.get('Date_Of_Birth'))
                    if not dob:
                        print(f"[SKIPPED] Invalid DOB in row: {row.to_dict()}")
                        continue
                    cursor.execute("""
                        INSERT INTO students 
                        (Student_ID, Student_Name, Date_Of_Birth, Department, Student_Email, Phone_Number, Address, Admission_Year)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        str(row.get('Student_ID', '')).upper(),
                        str(row.get('Student_Name', '')).upper(),
                        dob,
                        str(row.get('Department', '')).upper(),
                        str(row.get('Student_Email', '')).upper(),
                        str(row.get('Phone_Number', '')).upper(),
                        str(row.get('Address', '')).upper(),
                        str(row.get('Admission_Year', ''))
                    ))
                except mysql.connector.Error as e:
                    # print(f"[ERROR] insert_students row failed: {e} | Row: {row.to_dict()}")
                    continue
        print("[INFO] Inserted into students")

    @staticmethod
    def insert_teachers(df, conn):
        with conn.cursor() as cursor:
            for _, row in df.iterrows():
                try:
                    
                    cursor.execute("""
                        INSERT INTO teachers 
                        (Teacher_ID, Teacher_Name, Designation, Department, Teacher_Email, Phone_Number, Address, Joining_Year, Employment_Status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        str(row.get('Teacher_ID', '')).upper(),
                        str(row.get('Teacher_Name', '')).upper(),
                        str(row.get('Designation', '')).upper(),
                        str(row.get('Department', '')).upper(),
                        str(row.get('Teacher_Email', '')).upper(),
                        str(row.get('Phone_Number', '')).upper(),
                        str(row.get('Address', '')).upper(),
                        str(row.get('Joining_Year', '')).upper(),
                        str(row.get('Employment_Status', '')).upper()
                    ))
                except mysql.connector.Error as e:
                    # print(f"[ERROR] insert_teachers row failed: {e} | Row: {row.to_dict()}")
                    continue
        print("[INFO] Inserted into teachers")

    @staticmethod
    def insert_cash_book(df, conn):
        
        with conn.cursor() as cursor:
            for _, row in df.iterrows():
                try:
                    # print(row.get('Transaction_ID'))
                    T_date = UniversalProcessor.parse_date_safe(row.get('Transaction_Date'))
                    cursor.execute("""
                        INSERT INTO cash_book 
                        (Sl_No, Transaction_Id, Student_Id, Transaction_Date, Description, Transaction_Type, Amount, Credit, Debit, Balance)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        int(row.get('Sl_No', 0)),
                        str(row.get('Transaction_Id', '')).upper(),
                        str(row.get('Student_Id', '')).upper(),
                        T_date,
                        str(row.get('Description', '')).upper(),
                        str(row.get('Transaction_Type', '')).upper(),
                        row.get('Amount', ''),
                        row.get('Credit', ''),
                        row.get('Debit', ''),
                        row.get('Balance', 0)
                    ))
                except mysql.connector.Error as e:
                    # print(f"[ERROR] insert_cash_book row failed: {e} | Row: {row.to_dict()}")
                    continue
        print("[INFO] Inserted into cash_book")

    @staticmethod
    def insert_passedout_students(df, conn):
        with conn.cursor() as cursor:
            for _, row in df.iterrows():
                try:
                    cursor.execute("""
                        INSERT INTO passedout_students 
                        (SL_No, Student_ID, Student_Name, Certificate_No, Department, Student_Email, Phone_Number, Passedout_Year, Certificate)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        int(row.get('Sl_No', 0)),
                        str(row.get('Student_ID', '')).upper(),
                        str(row.get('Student_Name', '')).upper(),
                        str(row.get('Certificate_No', '')).upper(),
                        str(row.get('Department', '')).upper(),
                        str(row.get('Student_Email', '')).upper(),
                        str(row.get('Phone_Number', '')),
                        str(row.get('Passedout_Year', '')),
                        row.get('Certificate')
                    ))
                except mysql.connector.Error as e:
                    # print(f"[ERROR] insert_passedout_students row failed: {e} | Row: {row.to_dict()}")
                    continue
        print("[INFO] Inserted into passedout_students")

    @staticmethod
    def insert_teacher_borrowed_books(df, conn):
        with conn.cursor() as cursor:
            for _, row in df.iterrows():
                try:
                    borrow_date = UniversalProcessor.parse_date_safe(row.get('Borrow_Date'))
                    cursor.execute("""
                        INSERT INTO teacher_borrowed_books 
                        (Sl_No, Book_ID, Teacher_ID, Teacher_Name, Department, Book_Name, Author, Published_Year, Edition, Book_Price,
                        Borrow_Date, Borrow, Submit)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        int(row.get('Sl_No', 0)),
                        str(row.get('Book_ID', '')).upper(),
                        str(row.get('Teacher_ID', '')).upper(),
                        str(row.get('Teacher_Name', '')).upper(),
                        str(row.get('Department', '')).upper(),
                        str(row.get('Book_Name', '')).upper(),
                        str(row.get('Author', '')).upper(),
                        str(row.get('Published_Year', '')),
                        str(row.get('Edition', '')).upper(),
                        float(row.get('Book_Price', 0)),
                        borrow_date,
                        int(row.get('Borrow', 0)),
                        int(row.get('Submit', 0))
                    ))
                except mysql.connector.Error as e:
                    # print(f"[ERROR] insert_teacher_borrowed_books row failed: {e} | Row: {row.to_dict()}")
                    continue
        print("[INFO] Inserted into teacher_borrowed_books")

    @staticmethod
    def insert_borrowed_books(df, conn):
        with conn.cursor() as cursor:
            for _, row in df.iterrows():
                try:
                    borrow_date = UniversalProcessor.parse_date_safe(row.get('Borrow_Date'))
                    return_date = UniversalProcessor.parse_date_safe(row.get('Return_Date'))
                    cursor.execute("""
                        INSERT INTO borrowed_books 
                        (Sl_No, Book_ID, Student_ID, Student_Name, Student_Email, Department, Book_Name, Author, Published_Year, Edition,
                         Book_Price, Borrow_Date, Return_Date, Payable_Amount, Borrow, Submit, Renew, Payment_Status, Reminder)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        int(row.get('Sl_No', 0)),
                        str(row.get('Book_ID', '')).upper(),
                        str(row.get('Student_ID', '')).upper(),
                        str(row.get('Student_Name', '')).upper(),
                        str(row.get('Student_Email', '')).upper(),
                        str(row.get('Department', '')).upper(),
                        str(row.get('Book_Name', '')).upper(),
                        str(row.get('Author', '')).upper(),
                        str(row.get('Published_Year', '')),
                        str(row.get('Edition', '')).upper(),
                        str(row.get('Book_Price', 0)),
                        borrow_date,
                        return_date,
                        float(row.get('Payable_Amount', 0)),
                        int(row.get('Borrow', 0)),
                        int(row.get('Submit', 0)),
                        int(row.get('Renew', 0)),
                        str(row.get('Payment_Status', '')).upper(),
                        str(row.get('Reminder', '')).upper()
                    ))
                except mysql.connector.Error as e:
                    # print(f"[ERROR] insert_borrowed_books row failed: {e} | Row: {row.to_dict()}")
                    continue
        print("[INFO] Inserted into borrowed_books")

    # ============================ FILE HANDLER ============================

    @staticmethod
    def process_file(file_path, db_id):
        if not file_path.endswith(".xlsx"):
            print(f"[SKIPPED] Unsupported file format: {file_path}")
            return

        df = UniversalProcessor.read_excel(file_path)
        if df is None:
            return

        table = UniversalProcessor.detect_table_from_df(df)
        if table is None:
            print(f"[ERROR] Unknown table structure in file: {file_path}")
            return

        conn = database_connector.connect_to_db(f'{db_id}_library_db')
        if not conn:
            print(f"[ERROR] Database connection failed for ID: {db_id}")
            return

        try:
            getattr(UniversalProcessor, f"insert_{table}")(df, conn)
            conn.commit()
        except AttributeError:
            print(f"[WARNING] No insert handler for table: {table}")
        except mysql.connector.Error as e:
            conn.rollback()
            print("[ERROR] Insert failed:", e)
        finally:
            conn.close()
