import pandas as pd
import os


def Excel():
    # Define headers
    book_headers = [
        "Book_Name", "Author", "Published_Year", "Edition", "Publisher", "Place_of_Publication",
        "QTY", "Book_Price", "Order_Challan_Bill_Info", "Source"
    ]

    student_headers = [
        "Student_ID", "Student_Name", "Date_Of_Birth", "Standard", "Semester", "Department",
        "Student_Email", "Phone_Number", "Address", "Admission_Year"
    ]

    # Path setup
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    folder_name = "Library Excel Templates"
    folder_path = os.path.join(downloads_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    book_file_path = os.path.join(folder_path, "Book Stocks.xlsx")
    student_file_path = os.path.join(folder_path, "Student Details.xlsx")

    # Create empty DataFrames
    book_df = pd.DataFrame(columns=book_headers)
    student_df = pd.DataFrame(columns=student_headers)

    # Function to set column width based on header length
    def autofit_columns(worksheet, headers):
        for i, header in enumerate(headers):
            width = max(len(str(header)) + 2, 12)  # min width 12, padding +2
            worksheet.set_column(i, i, width)

    # Save Book Stocks with auto-fit column width
    with pd.ExcelWriter(book_file_path, engine='xlsxwriter') as writer:
        book_df.to_excel(writer, sheet_name='Books', index=False)
        worksheet = writer.sheets['Books']
        autofit_columns(worksheet, book_headers)

    # Save Student Details with auto-fit column width
    with pd.ExcelWriter(student_file_path, engine='xlsxwriter') as writer:
        student_df.to_excel(writer, sheet_name='Students', index=False)
        worksheet = writer.sheets['Students']
        autofit_columns(worksheet, student_headers)

    print("Excel files created with column widths auto-fitted to headers:")
    print(f"- {book_file_path}")
    print(f"- {student_file_path}")



# Excel()