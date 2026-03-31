import mysql.connector
import pandas as pd
import Logics.database_connector as database_connector
import Logics.migrate_data as migrate_data
from datetime import datetime, date
import Logics.books as assign

class STOCK:
    def read_excel(file_path):
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            print("Error reading Excel:", e)
            return None

    def insert_data(df, Id):
        conn = database_connector.connect_to_db(Id)
        if not conn:
            return
        try:
            cursor = conn.cursor()
            for _, row in df.iterrows():
                stock_date = date.today()
                stock_time = datetime.now().time()
                cursor.execute("""
                    INSERT INTO Book_Stock 
                    (Book_Name, Author, Published_Year, Edition, Publisher, Place_of_Publication, 
                    QTY, Book_Price, Order_Challan_Bill_Info, Source, Stock_Date, Stock_Time, Is_BookID_Assigned) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'NO')
                """, (
                    str(row['Book_Name']).upper(), str(row['Author']).upper(), row['Published_Year'], str(row['Edition']).upper(), str(row['Publisher']).upper(), 
                    str(row['Place_of_Publication']).upper(), row['QTY'], row['Book_Price'], 
                    str(row['Order_Challan_Bill_Info']).upper(), str(row['Source']).upper(), stock_date, stock_time
                ))
                conn.commit()
                assign.insert_books(Id, str(row['Book_Name']).upper(), str(row['Author']).upper())

            conn.commit()
            print("Data uploaded successfully!")
        except mysql.connector.Error as e:
            print("Error inserting data:", e)
        finally:
            conn.close()

    def process_files(file_path, Id):
        if file_path.endswith(".xlsx"):
            df = STOCK.read_excel(file_path)
            if df is not None:
                STOCK.insert_data(df, Id)
                
        else:
            print("Unsupported file format")

    def get_filepath(Id):
        while True:
            file_path = input("Enter file path (or type 'cancel' to exit): ").strip()
            if file_path.lower() == 'cancel':
                print("Operation cancelled.")
                break
            STOCK.process_files(file_path, Id)

    # Call the function with an ID (you can remove this if the function is called elsewhere)
    # get_filepath("User_ID")

class STUDENTS:
    def read_excel(file_path):
        try:
            df = pd.read_excel(file_path)
            # print(df)
            return df
        except Exception as e:
            print("Error reading Excel:", e)
            return None


    def convert_to_standard_date(dob_val):
        if isinstance(dob_val, (pd.Timestamp, datetime)):
            return dob_val.strftime('%Y-%m-%d')

        possible_formats = [
            '%d/%m/%Y', '%d-%m-%Y',
            '%Y/%m/%d', '%Y-%m-%d',
            '%m/%d/%Y', '%m-%d-%Y',
            '%d %b %Y', '%d %B %Y',
            '%b %d, %Y', '%B %d, %Y'
        ]

        for fmt in possible_formats:
            try:
                return datetime.strptime(str(dob_val), fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue

        raise ValueError(f"Date format for '{dob_val}' not recognized.")

    def insert_data(df, Id):
        conn = database_connector.connect_to_db(Id)
        if not conn:
            return

        try:
            cursor = conn.cursor()
            for _, row in df.iterrows():
                dob_val = row['Date_Of_Birth']
                try:
                    dob_converted = STUDENTS.convert_to_standard_date(dob_val)
                except ValueError as ve:
                    print(f"Skipping row due to invalid date format: {dob_val} — {ve}")
                    continue  # Skip this row if the date is invalid

                cursor.execute("""
                    INSERT INTO students (
                        Student_ID, Student_Name, Date_Of_Birth,  
                        Department, Student_Email, Phone_Number, Address, Admission_Year
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    str(row['Student_ID']).upper(),
                    str(row['Student_Name']).upper(),
                    dob_converted,
                    
                    str(row['Department']).upper(),
                    str(row['Student_Email']).upper(),
                    row['Phone_Number'],
                    str(row['Address']).upper(),
                    row['Admission_Year']
                ))
            conn.commit()
            print("Data uploaded successfully!")
        except mysql.connector.Error as e:
            print("Error inserting data:", e)
        finally:
            conn.close()



    def process_files(file_path, Id):
        if file_path.endswith(".xlsx"):
            df = STUDENTS.read_excel(file_path)
            if df is not None:
                STUDENTS.insert_data(df, Id)
        else:
            print("Unsupported file format")

    def get_filepath(Id):
        while True:
            file_path = input("Enter file path (or type 'cancel' to exit): ").strip()
            if file_path.lower() == 'cancel':
                print("Operation cancelled.")
                break
            STUDENTS.process_files(file_path, Id)

    # Call the function with an ID (you can remove this if the function is called elsewhere)
    # get_filepath("User_ID")

class BOOK_ID_ASSIGN:
    def read_excel(file_path):
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            print("Error reading Excel:", e)
            return None

    def fetch_additional_fields(conn, book_name, author):
        cursor = conn.cursor()
        cursor.execute("SELECT Published_Year, Edition, Book_Price FROM book_stock WHERE Book_Name = %s AND Author = %s", (book_name, author))
        row = cursor.fetchone()
        if row:
            return row  # Return the necessary fields
        else:
            print(f"Book '{book_name}' by {author} not found in book_stocks.")
            return None

    def insert_data(df, Id):
        conn = database_connector.connect_to_db(Id)
        if not conn:
            return
        try:
            cursor = conn.cursor()
            for _, row in df.iterrows():
                additional_fields = BOOK_ID_ASSIGN.fetch_additional_fields(conn, row['Book_Name'], row['Author'])
                if additional_fields:
                    cursor.execute("""
                        INSERT INTO books (Book_ID, Book_Name, Author, Published_Year, Edition, Book_Price, Stock_Status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        row['Book_ID'], row['Book_Name'], row['Author'], additional_fields[0], additional_fields[1], additional_fields[2], "In Stock"
                    ))
            conn.commit()
            print("Data uploaded successfully!")
        except mysql.connector.Error as e:
            print("Error inserting data:", e)   
        finally:
            conn.close()

    def process_files(file_path, Id):
        if file_path.endswith(".xlsx"):
            df = BOOK_ID_ASSIGN.read_excel(file_path)
            if df is not None:
                BOOK_ID_ASSIGN.insert_data(df, Id)
        else:
            print("Unsupported file format")

    def get_filepath(Id):
        while True:
            file_path = input("Enter file path (or type 'cancel' to exit): ").strip()
            if file_path.lower() == 'cancel':
                print("Operation cancelled.")
                break
            BOOK_ID_ASSIGN.process_files(file_path, Id)
class TEACHERS:
    def read_excel(file_path):
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            print("Error reading Excel:", e)
            return None

    def insert_data(df, Id):
        conn = database_connector.connect_to_db(Id)
        if not conn:
            return

        try:
            cursor = conn.cursor()
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO Teachers (
                        Teacher_ID, Teacher_Name, Designation, Department, 
                        Teacher_Email, Phone_Number, Address, Joining_Year, Employment_Status
                    ) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    str(row['Teacher_ID']).upper(),
                    str(row['Teacher_Name']).upper(),
                    str(row['Designation']).upper(),
                    str(row['Department']).upper(),
                    str(row['Teacher_Email']).upper(),
                    row['Phone_Number'],
                    str(row['Address']).upper(),
                    str(row['Joining_Year']),
                    str(row['Employment_Status']).upper()
                ))
            conn.commit()
            print("✅ Teacher data uploaded successfully!")
        except mysql.connector.Error as e:
            print("❌ Error inserting teacher data:", e)
        finally:
            conn.close()

    def process_files(file_path, Id):
        if file_path.endswith(".xlsx"):
            df = TEACHERS.read_excel(file_path)
            if df is not None:
                TEACHERS.insert_data(df, Id)
        else:
            print("❌ Unsupported file format")

    def get_filepath(Id):
        while True:
            file_path = input("Enter Excel file path (or type 'cancel' to exit): ").strip()
            if file_path.lower() == 'cancel':
                print("Operation cancelled.")
                break
            TEACHERS.process_files(file_path, Id)

def execute_migration(cursor, connection, Book_Name, Author, BookID):
    migrate_data.migrate_data(cursor, connection, Book_Name, Author, BookID)
