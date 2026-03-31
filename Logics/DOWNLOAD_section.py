import pandas as pd
import os
import openpyxl
import re
import Logics.database_connector as database_connector
# import database_connector as database_connector

class View:
    @staticmethod
    def get_teachers(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers")
        teachers = cursor.fetchall()
        teacher_list = []
        for teacher in teachers:
            teacher_info = [
                teacher[0],  # Teacher_ID
                teacher[1],  # Teacher_Name
                teacher[2],  # Designation
                teacher[3],  # Department
                teacher[4],  # Teacher_Email
                teacher[5],  # Phone_Number
                teacher[6],  # Address
                teacher[7],  # Joining_Year
                teacher[8]  # Employment_Status
            ]
            teacher_list.append(teacher_info)
        cursor.close()
        conn.close()
        return teacher_list

    @staticmethod
    def get_students(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        student_list = []
        for student in students:
            student_info = [
                student[0],  
                student[1],  
                student[2],  
                student[3],  
                student[4], 
                student[5], 
                student[6],  
                student[7]  
                
            ]
            student_list.append(student_info)
        cursor.close()
        conn.close()
        return student_list

    @staticmethod
    def get_book_stock(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM book_stock")
        books = cursor.fetchall()
        book_list = []
        for book in books:
            book_info = [
                # book[0],  # SL_No
                book[1],  # Book_Name
                book[2],  # Author
                book[3],  # Edition
                book[4],  # Publisher
                book[5],  # Place_of_Publication
                book[6],  # Published_Year
                book[7],  # QTY
                book[8],  # Book_Price
                book[9],  # Order_Challan_Bill_Info
                book[10], # Source
                book[11], # Stock_Date
                # book[12]  # Stock_Time
            ]
            book_list.append(book_info)
        cursor.close()
        conn.close()
        return book_list

    @staticmethod
    def get_books(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        
        book_list = []
        for book in books:
            book_info = [
                book[0],  # Book_ID
                book[1],  # Book_Name
                book[2],  # Author
                book[3],  # Published_Year
                book[4],  # Edition
                book[5],  # Book_Price
                book[6]   # Stock_Status
            ]
            book_list.append(book_info)
        cursor.close()
        conn.close()
        return book_list
    
    @staticmethod
    def get_borrowed_books(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM borrowed_books")
        borrowed_books = cursor.fetchall()
        borrowed_books_list = []
        for book in borrowed_books:
            book_info = [
                book[0],  # Sl_No
                book[1],  # Book_ID
                book[2],  # Student_ID
                book[3],  # Student_Name
                book[4],  # Student_Email
                book[5],  # Book_Name
                book[6],  # Author
                book[7],  # Published_Year
                book[8],  # Edition
                book[9],  # Book_Price
                book[10], # Borrow_Date
                book[11], # Return_Date
                book[12], # Payable_Amount
                book[13], # Borrow
                book[14], # Submit
                book[15], # Renew
                book[16], # Payment_Status
                book[17],
                book[18]
            ]
            borrowed_books_list.append(book_info)
        cursor.close()
        conn.close()
        return borrowed_books_list

    @staticmethod
    def get_passedout_students(Id):
        """
        Fetches all records from the passedout_students table for the given institution ID.

        Parameters:
            Id (str): Institution ID used to connect to the correct database.

        Returns:
            List[List]: A list of student data rows (each as a list).
        """
        try:
            conn = database_connector.connect_to_db(f"{Id}_library_db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM passedout_students")
            passedout_data = cursor.fetchall()
            passedout_students_list = []

            for student in passedout_data:
                student_info = [
                    # student[0],  # SL_No
                    student[1],  # Student_ID
                    student[2],  # Student_Name
                    student[3],  # Certificate_No
                    student[4],  # Department
                    student[5],  # Student_Email
                    student[6],  # Phone_Number
                    student[7]  # Passedout_Year
                ]
                passedout_students_list.append(student_info)

            return passedout_students_list

        except Exception as e:
            print(f"❌ Error in get_passedout_students: {e}")
            return []

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()


    @staticmethod
    def get_cash_transactions(Id):
        
        try:
            conn = database_connector.connect_to_db(f"{Id}_library_db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cash_book")
            transactions_data = cursor.fetchall()
            cash_transactions_list = []

            for transaction in transactions_data:
                transaction_info = [
                    # transaction[0],  
                    transaction[1], 
                    transaction[2],  
                    transaction[3], 
                    transaction[4],  
                    transaction[5],
                    transaction[6],
                    transaction[7],
                    transaction[8],
                    transaction[9]   
                ]
                cash_transactions_list.append(transaction_info)

            return cash_transactions_list

        except Exception as e:
            print(f"❌ Error in get_cash_transactions: {e}")
            return []

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
            
    def get_teacher_borrowed_books(Id):
        conn = database_connector.connect_to_db(f"{Id}_library_db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Teacher_Borrowed_Books")
        borrowed_books = cursor.fetchall()
        
        borrowed_books_list = []
        for book in borrowed_books:
            book_info = [
                book[0],  # Sl_No
                book[1],  # Book_ID
                book[5],  # Book_Name
                book[6],  # Author
                book[7],  # Published_Year
                book[8],  # Edition
                book[9],  # Book_Price
                book[2],  # Teacher_ID
                book[3],  # Teacher_Name
                book[4],  # Department
                book[10], # Borrow_Date
                book[11], # Borrow
                book[12]  # Submit
            ]
            borrowed_books_list.append(book_info)

        cursor.close()
        conn.close()
        return borrowed_books_list

class excel:
    folder_path = os.path.join(os.path.expanduser("~"), "Downloads")  # Default download folder

    
    @staticmethod
    def set_folder_path():
        # Ensure the folder exists
        if not os.path.exists(excel.folder_path):
            os.makedirs(excel.folder_path)
    
    @staticmethod
    def change_folder_path(new_path):
        # Change the folder path and create the folder if necessary
        excel.folder_path = new_path
        if not os.path.exists(excel.folder_path):
            os.makedirs(excel.folder_path)
    
    @staticmethod
    def download_books_excel(data, Book_Name=None, Author=None, Published_Year=None, Stock_Status=None, filename=None):
        """
        Export books data to Excel with optional filtering by multiple fields.
        Filters by Book_ID, Book_Name, Author, Published_Year, and Stock_Status.
        Automatically generates filename based on filters if not provided.
        Normalizes Stock_Status (✔️/❌/🚫) and adjusts column widths.
        """

        # Ensure export folder is set
        excel.set_folder_path()
        if not excel.folder_path:
            raise RuntimeError("Excel folder path is not set!")

        headers = ["Book_ID", "Book_Name", "Author", "Published_Year", "Edition", "Book_Price", "Stock_Status"]
        df = pd.DataFrame(data, columns=headers)

        # Apply filters
        if Book_Name is not None:
            df = df[df["Book_Name"].str.contains(Book_Name, case=False, na=False)]
        if Author is not None:
            df = df[df["Author"].str.contains(Author, case=False, na=False)]
        if Published_Year is not None:
            df = df[df["Published_Year"].astype(str) == str(Published_Year)]
        if Stock_Status is not None:
            status_lower = str(Stock_Status).strip().lower()
            if status_lower == "others":
                df = df[~df["Stock_Status"].astype(str).str.lower().isin(
                    ["1", "available", "in stock", "yes", "0", "not available", "out of stock", "no"]
                )]
            else:
                df = df[df["Stock_Status"].astype(str).str.lower() == status_lower]

        # Normalize Stock_Status
        if "Stock_Status" in df.columns:
            df["Stock_Status"] = df["Stock_Status"].apply(
                lambda x: "✔️" if str(x).strip().lower() in ("1", "available", "in stock", "yes")
                else ("❌" if str(x).strip().lower() in ("0", "unavailable", "out of stock", "no")
                    else "🚫")
            )

        # Auto-generate and sanitize filename
        if not filename:
            parts = []
            if Book_Name: parts.append(f"Name_{Book_Name}")
            if Author: parts.append(f"Author_{Author}")
            if Published_Year: parts.append(f"Year_{Published_Year}")
            if Stock_Status: parts.append(f"Status_{Stock_Status}")
            filename = "Books_Report.xlsx" if not parts else f"Books_{'_'.join(parts)}.xlsx"

        # Remove invalid characters for Windows filenames
        filename = re.sub(r'[\\/*?:"<>|()\s]+', '_', filename)

        # Final file path
        filepath = os.path.join(excel.folder_path, filename)

        # Handle locked file (try new names if open)
        counter = 1
        while True:
            try:
                df.to_excel(filepath, index=False)
                break
            except PermissionError:
                filepath = os.path.join(excel.folder_path, f"{os.path.splitext(filename)[0]}_{counter}.xlsx")
                counter += 1

        # Auto-adjust column widths
        excel._set_column_width(filepath)

        print(f"Excel file '{filepath}' has been downloaded successfully with applied filters.")
        return True





    @staticmethod
    def download_students_excel(data, Department=None, Admission_Year=None, filename=None):
        """
        Export students data to Excel with optional filtering by Department and Admission Year.
        Automatically ignores leading/trailing spaces in inputs and data.
        """

        # Ensure export folder is ready
        excel.set_folder_path()
        if not excel.folder_path:
            raise RuntimeError("Excel folder path is not set!")

        headers = ["Student_ID", "Student_Name", "Date_Of_Birth", "Department",
                "Student_Email", "Phone_Number", "Address", "Admission_Year"]
        df = pd.DataFrame(data, columns=headers)

        # Normalize both inputs (strip spaces) and DataFrame columns for comparison
        if Department is not None:
            Department = str(Department).strip()
            df["Department"] = df["Department"].astype(str).str.strip()
            df = df[df["Department"].str.lower() == Department.lower()]

        if Admission_Year is not None:
            Admission_Year = str(Admission_Year).strip()
            df["Admission_Year"] = df["Admission_Year"].astype(str).str.strip()
            df = df[df["Admission_Year"] == Admission_Year]

        # If no data left after filtering
        if df.empty:
            print("⚠️ No student records found for the given filters. No file created.")
            return False

        # Generate filename dynamically
        if not filename:
            parts = []
            if Department: parts.append(f"Dept_{Department}")
            if Admission_Year: parts.append(f"Year_{Admission_Year}")
            filename = "Students_Report.xlsx" if not parts else f"Students_{'_'.join(parts)}.xlsx"

        # Sanitize filename for Windows
        filename = re.sub(r'[\\/*?:"<>|()\s]+', '_', filename)

        # Final file path
        filepath = os.path.join(excel.folder_path, filename)

        # Handle file-in-use conflicts (if Excel file is open)
        counter = 1
        while True:
            try:
                df.to_excel(filepath, index=False)
                break
            except PermissionError:
                filepath = os.path.join(excel.folder_path, f"{os.path.splitext(filename)[0]}_{counter}.xlsx")
                counter += 1

        # Adjust column widths
        excel._set_column_width(filepath)

        print(f"Excel file '{filepath}' has been downloaded successfully with applied filters.")
        return True

    
    @staticmethod
    def download_stocks_excel(data,Book_Name=None,Author=None,Publisher=None,
                              Place_of_Publication=None,Source=None,Stock_Date=None,
                              Published_Year=None,Order_Challan_Bill_Info=None,filename=None):
        """
        Export book stock data to Excel with optional filtering by:
        Book Name, Author, Publisher, Place of Publication, Source,
        Stock Date, Published Year, and Order/Challan/Bill Info.
        Automatically trims spaces and performs case-insensitive exact matching.
        """

        # Ensure export folder is ready
        excel.set_folder_path()
        if not excel.folder_path:
            raise RuntimeError("Excel folder path is not set!")

        headers = ["Book_Name", "Author","Edition", "Publisher",
                   "Place_of_Publication", "Published_Year","QTY", "Book_Price", 
                   "Order_Challan_Bill_Info", "Source", "Stock_Date"]

        # Limit to first 11 columns (in case extra fields exist in data)
        df = pd.DataFrame([row[:11] for row in data], columns=headers)
        # print(df)
        # Helper for filtering
        def apply_filter(df, column, value):
            if value is not None:
                value = str(value).strip()
                df[column] = df[column].astype(str).str.strip()
                return df[df[column].str.lower() == value.lower()]
            return df

        # Apply filters one by one
        df = apply_filter(df, "Book_Name", Book_Name)
        df = apply_filter(df, "Author", Author)
        df = apply_filter(df, "Publisher", Publisher)
        df = apply_filter(df, "Place_of_Publication", Place_of_Publication)
        df = apply_filter(df, "Source", Source)
        df = apply_filter(df, "Stock_Date", Stock_Date)
        df = apply_filter(df, "Published_Year", Published_Year)
        df = apply_filter(df, "Order_Challan_Bill_Info", Order_Challan_Bill_Info)

        # If no records left after filtering
        if df.empty:
            print("⚠️ No book stock records found for the given filters. No file created.")
            return False

        # Generate filename dynamically if not provided
        if not filename:
            parts = []
            if Book_Name: parts.append(f"Book_{Book_Name}")
            if Author: parts.append(f"Author_{Author}")
            if Publisher: parts.append(f"Publisher_{Publisher}")
            if Place_of_Publication: parts.append(f"Place_{Place_of_Publication}")
            if Source: parts.append(f"Source_{Source}")
            if Stock_Date: parts.append(f"Date_{Stock_Date}")
            if Published_Year: parts.append(f"Year_{Published_Year}")
            if Order_Challan_Bill_Info: parts.append(f"Bill_{Order_Challan_Bill_Info}")

            filename = "Book_Stock_Report.xlsx" if not parts else f"Book_Stock_{'_'.join(parts)}.xlsx"

        # Sanitize filename (remove invalid characters for Windows)
        filename = re.sub(r'[\\/*?:"<>|()\s]+', '_', filename)

        # Final file path
        filepath = os.path.join(excel.folder_path, filename)

        # Handle file-in-use conflicts (create a new version if file is open)
        counter = 1
        while True:
            try:
                df.to_excel(filepath, index=False)
                break
            except PermissionError:
                filepath = os.path.join(excel.folder_path, f"{os.path.splitext(filename)[0]}_{counter}.xlsx")
                counter += 1

        # Adjust column widths
        excel._set_column_width(filepath)

        print(f"Excel file '{filepath}' has been downloaded successfully with applied filters.")
        return True
    

    @staticmethod
    def download_borrowed_books_excel(data, start_date=None, end_date=None, filename="Borrowed_Books_Report.xlsx"):
        """
        Export borrowed books to Excel with optional date filtering.
        """
        excel.set_folder_path()
        if not excel.folder_path:
            raise RuntimeError("Excel folder path is not set!")

        # Adjust filename if a date range is given
        if start_date and end_date:
            filename = f"Borrowed_Books_{start_date}_to_{end_date}.xlsx"

        headers = ["Sl_No", "Book_ID", "Student_ID", 
                "Student_Name", "Student_Email", "Department",
                "Book_Name", "Author", "Published_Year", "Edition", "Book_Price",
                "Borrow_Date", "Return_Date", "Payable_Amount", "Borrow", 
                "Submit", "Renew", "Payment_Status", "Reminder"]

        df = pd.DataFrame(data, columns=headers)

        # Convert to datetime for filtering
        df["Borrow_Date"] = pd.to_datetime(df["Borrow_Date"], errors="coerce")
        df["Return_Date"] = pd.to_datetime(df["Return_Date"], errors="coerce")

        # Save original string dates for logging
        start_str, end_str = start_date, end_date

        # Apply filtering
        if start_date:
            start_date = pd.to_datetime(start_date)
            df = df[df["Borrow_Date"] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date)
            df = df[df["Borrow_Date"] <= end_date]

        # Replace numeric flags with checkmarks
        for col in ["Borrow", "Submit", "Renew"]:
            df[col] = df[col].apply(lambda x: "✔️" if x == 1 else "")

        # Save to Excel
        filepath = os.path.join(excel.folder_path, filename)
        df.to_excel(filepath, index=False)
        excel._set_column_width(filepath)

        print(f"Excel file '{filepath}' has been downloaded successfully "
            f"for period {start_str or 'Beginning'} to {end_str or 'Today'}.")
        return True


    @staticmethod
    def download_borrowed_books_excel1(data, filename="Borrowed_Books_Report.xlsx"):
        headers = ["Sl_No", "Book_ID", "Student_ID", 
                "Student_Name", "Student_Email", "Department",
                "Book_Name", "Author", "Published_Year", "Edition", "Book_Price",
                "Borrow_Date", "Return_Date", "Payable_Amount", "Borrow", 
                "Submit", "Renew", "Payment_Status", "Reminder"]

        df = pd.DataFrame(data, columns=headers)
        excel.set_folder_path()
        filepath = os.path.join(excel.folder_path, filename)
        df.to_excel(filepath, index=False)
        excel._set_column_width(filepath)

        print(f"Excel file '{filepath}' has been downloaded successfully.")
        return True
    @staticmethod
    def download_passedout_students_excel(data, filename="Passedout_Students_Report.xlsx"):
        headers = ["Student_ID", "Student_Name", "Certificate_No", "Department",
                "Student_Email", "Phone_Number", "Passedout_Year"]
        df = pd.DataFrame(data, columns=headers)
        excel.set_folder_path()
        filepath = os.path.join(excel.folder_path, filename)
        df.to_excel(filepath, index=False)
        excel._set_column_width(filepath)
        print(f"Excel file '{filepath}' has been downloaded successfully.")
        return True
    
    
    @staticmethod
    def download_teachers_excel(data, Department=None, Designation=None, Joining_Year=None, Employment_Status=None, filename=None):
        """
        Export teacher data to Excel with optional filtering by Department, Designation,
        Joining Year, and Employment Status.
        Automatically ignores leading/trailing spaces in inputs and data.
        """

        # Ensure export folder is ready
        excel.set_folder_path()
        if not excel.folder_path:
            raise RuntimeError("Excel folder path is not set!")

        headers = ["Teacher_ID", "Teacher_Name", "Designation", "Department", 
                "Teacher_Email", "Phone_Number", "Address", 
                "Joining_Year", "Employment_Status"]
        df = pd.DataFrame(data, columns=headers)

        # Normalize inputs (strip spaces) and DataFrame columns for comparison
        if Department is not None:
            Department = str(Department).strip()
            df["Department"] = df["Department"].astype(str).str.strip()
            df = df[df["Department"].str.lower() == Department.lower()]

        if Designation is not None:
            Designation = str(Designation).strip()
            df["Designation"] = df["Designation"].astype(str).str.strip()
            df = df[df["Designation"].str.lower() == Designation.lower()]

        if Joining_Year is not None:
            Joining_Year = str(Joining_Year).strip()
            df["Joining_Year"] = df["Joining_Year"].astype(str).str.strip()
            df = df[df["Joining_Year"] == Joining_Year]

        if Employment_Status is not None:
            Employment_Status = str(Employment_Status).strip()
            df["Employment_Status"] = df["Employment_Status"].astype(str).str.strip()
            df = df[df["Employment_Status"].str.lower() == Employment_Status.lower()]

        # If no data left after filtering
        if df.empty:
            print("⚠️ No teacher records found for the given filters. No file created.")
            return False

        # Generate filename dynamically
        if not filename:
            parts = []
            if Department: parts.append(f"Dept_{Department}")
            if Designation: parts.append(f"Designation_{Designation}")
            if Joining_Year: parts.append(f"Year_{Joining_Year}")
            if Employment_Status: parts.append(f"Status_{Employment_Status}")
            filename = "Teachers_Report.xlsx" if not parts else f"Teachers_{'_'.join(parts)}.xlsx"

        # Sanitize filename for Windows
        filename = re.sub(r'[\\/*?:"<>|()\s]+', '_', filename)

        # Final file path
        filepath = os.path.join(excel.folder_path, filename)

        # Handle file-in-use conflicts (if Excel file is open)
        counter = 1
        while True:
            try:
                df.to_excel(filepath, index=False)
                break
            except PermissionError:
                filepath = os.path.join(excel.folder_path, f"{os.path.splitext(filename)[0]}_{counter}.xlsx")
                counter += 1

        # Adjust column widths
        excel._set_column_width(filepath)

        print(f"Excel file '{filepath}' has been downloaded successfully with applied filters.")
        return True

    
    @staticmethod
    def download_passedout_students_excel(data,Department=None,Passedout_Year=None,filename=None):
        """
        Export passed-out students data to Excel with optional filtering by Department and Passedout_Year.
        Automatically generates filename based on filters if not provided.
        Handles locked files and adjusts column widths like other export functions.
        """
        # Ensure export folder is set
        excel.set_folder_path()
        if not excel.folder_path:
            raise RuntimeError("Excel folder path is not set!")

        headers = [
            "Student_ID", "Student_Name", "Certificate_No",
            "Department", "Student_Email", "Phone_Number", "Passedout_Year"
        ]
        df = pd.DataFrame(data, columns=headers)

        # Apply filters
        if Department is not None:
            df = df[df["Department"].str.contains(Department.upper())]
        if Passedout_Year is not None:
            df = df[df["Passedout_Year"].astype(str) == str(Passedout_Year)]

        # Auto-generate and sanitize filename
        if not filename:
            parts = []
            if Department: parts.append(f"Department Of ({Department.title()})")
            if Passedout_Year: parts.append(f"Year ({Passedout_Year})")
            filename = "Passedout_Students_Report.xlsx" if not parts else f"Passedout Students {' '.join(parts)}.xlsx"

        # Remove invalid characters for Windows filenames
        filename = re.sub(r'[\\/*?:"<>|()\s]+', ' ', filename)

        # Final file path
        filepath = os.path.join(excel.folder_path, filename)

        # Handle locked file (rename if open)
        counter = 1
        while True:
            try:
                df.to_excel(filepath, index=False)
                break
            except PermissionError:
                filepath = os.path.join(
                    excel.folder_path,
                    f"{os.path.splitext(filename)[0]}_{counter}.xlsx"
                )
                counter += 1

        # Auto-adjust column widths
        excel._set_column_width(filepath)

        print(f"Excel file '{filepath}' has been downloaded successfully with applied filters.")
        return True

    @staticmethod
    def download_teacher_borrowed_books_excel(data, start_date=None, end_date=None, filename="Teacher_Borrowed_Books_Report.xlsx"):
        """
        Export teacher borrowed books to Excel with optional date range filtering.
        If the file is already open, automatically saves as a new version (_1, _2, ...).
        """
        excel.set_folder_path()
        if not excel.folder_path:
            raise RuntimeError("Excel folder path is not set!")

        if start_date and end_date:
            filename = f"Teacher_Borrowed_Books_{start_date}_to_{end_date}.xlsx"

        headers = ["Sl_No", "Book_ID", "Teacher_ID", 
                "Teacher_Name", "Department", "Book_Name", "Author",
                "Published_Year", "Edition", "Book_Price", "Borrow_Date",
                "Borrow", "Submit"]

        df = pd.DataFrame(data, columns=headers)

        df["Borrow_Date"] = pd.to_datetime(df["Borrow_Date"], errors="coerce")

        start_str, end_str = start_date, end_date
        if start_date:
            start_date = pd.to_datetime(start_date)
            df = df[df["Borrow_Date"] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date)
            df = df[df["Borrow_Date"] <= end_date]

        for col in ["Borrow", "Submit"]:
            df[col] = df[col].apply(lambda x: "✔️" if x == 1 else "")

        filepath = os.path.join(excel.folder_path, filename)

        # Retry logic: create a new version if file is locked
        counter = 1
        while True:
            try:
                df.to_excel(filepath, index=False)
                break
            except PermissionError:
                base, ext = os.path.splitext(filepath)
                filepath = f"{base}_{counter}{ext}"
                counter += 1

        excel._set_column_width(filepath)

        print(f"Excel file '{filepath}' has been downloaded successfully "
            f"for period {start_str or 'Beginning'} to {end_str or 'Today'}.")
        return True



        
    @staticmethod
    def _set_column_width(filepath):
        # Helper method to adjust column widths
        wb = openpyxl.load_workbook(filepath)
        ws = wb.active
        for col in ws.columns:
            max_length = 145 // 7  # Set max column width
            column = col[0].column_letter
            ws.column_dimensions[column].width = max_length
        wb.save(filepath)

# View.get_cash_transactions(306892)


# data = View.get_students("877509")
# excel.download_students_excel(data, Department="ELECTRONICS & TELECOMMUNICATION  ENGINEERING", Admission_Year=None, filename=None)