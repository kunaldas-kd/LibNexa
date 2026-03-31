# === Importing required modules ===
import os
import sys
import time
import platform
import re
import ctypes
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
 
# === Import custom database logic ===
import Logics.view_database
import Logics.database_connector as database_connector
 
# === Define Google Drive access scope ===
SCOPES = ['https://www.googleapis.com/auth/drive.file']
 
# === PyInstaller path resolver: gets actual path even in compiled EXE ===
def get_absolute_path(relative_path):
    if getattr(sys, 'frozen', False):  # Running as EXE
        base_path = sys._MEIPASS  # PyInstaller temp folder
    else:
        base_path = os.path.abspath(".")  # Script mode
    return os.path.join(base_path, relative_path)
 
# === Get fixed token save path (persistent location, not temp) ===
# === Updated Token Directory (avoid restricted folders) ===
# import os
# import platform
# import ctypes

def get_user_token_dir():
    if platform.system() == "Windows":
        documents = os.path.join(os.path.expanduser("~"), "Documents")
        libnest_dir = os.path.join(documents, 'LibNest')
        token_dir = os.path.join(libnest_dir, 'tokens')

        # Create both directories
        os.makedirs(token_dir, exist_ok=True)

        # Set both folders as hidden
        FILE_ATTRIBUTE_HIDDEN = 0x02
        try:
            ctypes.windll.kernel32.SetFileAttributesW(libnest_dir, FILE_ATTRIBUTE_HIDDEN)
            ctypes.windll.kernel32.SetFileAttributesW(token_dir, FILE_ATTRIBUTE_HIDDEN)
        except Exception as e:
            print(f"Failed to hide folder(s) on Windows: {e}")

        return token_dir

    else:
        # On Linux/macOS: Use hidden folder names (starting with dot)
        libnest_dir = os.path.expanduser("~/.libnest")
        token_dir = os.path.join(libnest_dir, ".tokens")
        os.makedirs(token_dir, exist_ok=True)

        return token_dir

    


# === Sanitize email to valid filename ===
def sanitize_filename(name):
    return re.sub(r'[^\w\-_.]', '_', name)
 
# === Save Pandas DataFrame to Excel file ===
def save_excel(df, filename):
    folder_path = get_absolute_path("exports")  # Excel export folder
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, filename)
    df.to_excel(filepath, index=False)  # Save as .xlsx
    return filepath
 
# === Generate Excel reports from different datasets ===
def download_books_excel(data, filename="Books_Report.xlsx"):
    headers = ["Book_ID", "Book_Name", "Author", "Published_Year", "Edition", "Book_Price", "Stock_Status"]
    df = pd.DataFrame(data, columns=headers)
    return save_excel(df, filename)
 
def download_students_excel(data, filename="Students_Report.xlsx"):
    headers = ["Student_ID", "Student_Name", "Date_Of_Birth", "Department",
               "Student_Email", "Phone_Number", "Address", "Admission_Year"]
    df = pd.DataFrame(data, columns=headers)
    return save_excel(df, filename)
 
def download_stocks_excel(data, filename="Book_Stock_Report.xlsx"):
    headers =["SL_No", "Book_Name", "Author", "Edition", "Publisher", "Place_of_Publication",
            "Published_Year", "QTY", "Book_Price", "Order_Challan_Bill_Info", "Source",
            "Stock_Date", "Stock_Time", "Is_BookID_Assigned"]

    df = pd.DataFrame(data, columns=headers)
    return save_excel(df, filename)
 
def download_borrowed_books_excel(data, filename="Borrowed_Books_Report.xlsx"):
    headers = ["Sl_No", "Book_ID", "Student_ID","Student_Name", "Student_Email", "Department",
               "Book_Name", "Author", "Published_Year", "Edition", "Book_Price", "Borrow_Date", 
               "Return_Date", "Payable_Amount", "Borrow", "Submit", "Renew", "Payment_Status", "Reminder"]
    df = pd.DataFrame(data, columns=headers)
    return save_excel(df, filename)
 
def download_passedout_students_excel(data, filename="Passedout_Students_Report.xlsx"):
    headers = ["SL_No", "Student_ID", "Student_Name", "Certificate_No", "Department",
               "Student_Email", "Phone_Number", "Passedout_Year", "Certificate"]
    # df = pd.DataFrame([row[:8] for row in data], columns=headers)
    df = pd.DataFrame(data, columns=headers)
    return save_excel(df, filename)
 
def download_teachers_excel(data, filename="Teachers_Report.xlsx"):
    headers = ["Teacher_ID", "Teacher_Name", "Designation", "Department",
               "Teacher_Email", "Phone_Number", "Address", "Joining_Year", "Employment_Status"]
    df = pd.DataFrame(data, columns=headers)
    return save_excel(df, filename)

def download_teacher_borrowed_books_excel(data, filename="Borrowed_Books_Report_Of_Teachers.xlsx"):
    headers = ["Sl_No", "Book_ID", "Teacher_ID", "Teacher_Name", "Department",
               "Book_Name", "Author", "Published_Year", "Edition",
               "Book_Price", "Borrow_Date", "Borrow", "Submit"]
    df = pd.DataFrame(data, columns=headers)
    return save_excel(df, filename)

def download_cashbook_excel(data, filename="Cash_Book.xlsx"):
    headers = ["Sl_No", "Transaction_Id", "Student_Id", "Transaction_Date",
                   "Description", "Transaction_Type", "Amount", "Credit", "Debit","Balance"]
    df = pd.DataFrame(data, columns=headers)
    return save_excel(df, filename)

# === Google Drive login with auto-refresh and persistent token ===
def get_drive_credentials(user_email):
    token_dir = get_user_token_dir()
    os.makedirs(token_dir, exist_ok=True)  # Ensure directory exists
 
    safe_email = sanitize_filename(user_email)  # Clean filename
    token_path = os.path.join(token_dir, f"{safe_email}_token.json")  # Where user token is saved
    credentials_file = get_absolute_path("Logics/credentials.json")  # OAuth credentials
 
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)  # Load token
 
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())  # Auto refresh token silently
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())
    elif not creds or not creds.valid:
        # First-time login required
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        try:
            creds = flow.run_local_server(port=0)  # Show browser popup
        except:
            if platform.system() == "Windows":
                ctypes.windll.kernel32.AllocConsole()  # Show console if no browser
            creds = flow.run_console()
 
        # Save new token
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())
 
    return creds
 
# === Upload a single file to user’s Google Drive ===
def upload_file_to_drive(library_id, file_path):
    db_name = f"{library_id}_library_db"
    connection = database_connector.connect_to_db(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT Institute_Email FROM users")  # Get user email from DB
    email = cursor.fetchone()[0]
 
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
 
    creds = get_drive_credentials(email)  # Use that email for token
    service = build('drive', 'v3', credentials=creds)
 
    file_name = os.path.basename(file_path)
    mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
 
    # Check if file already exists on Drive
    query = f"name = '{file_name}' and mimeType = '{mime_type}' and trashed = false"
    result = service.files().list(q=query, fields="files(id, name)").execute()
    files = result.get('files', [])
    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
 
    if files:
        file_id = files[0]['id']
        service.files().update(fileId=file_id, media_body=media).execute()  # Update if exists
        view_link = service.files().get(fileId=file_id, fields='webViewLink').execute()['webViewLink']
        return view_link
    else:
        file_metadata = {'name': file_name, 'mimeType': mime_type}
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        return file.get('webViewLink')
 
# === Upload all exported Excel reports ===
# import pandas as pd

def upload_exports_folder(library_id):
    exports_dir = get_absolute_path("exports")
    if not os.path.exists(exports_dir):
        raise FileNotFoundError("exports folder not found.")
 
    uploaded_links = []
    for file_name in os.listdir(exports_dir):
        file_path = os.path.join(exports_dir, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.xlsx'):
            try:
                df = pd.read_excel(file_path)

                # Skip if DataFrame has only headers (i.e., 0 rows)
                if df.shape[0] == 0:
                    print(f"Skipping file {file_name}: Only headers, no data rows.")
                    continue

            except Exception as e:
                print(f"Skipping file {file_name}: {e}")
                continue

            link = upload_file_to_drive(library_id, file_path)
            uploaded_links.append((file_name, link))

    return uploaded_links

 
# === Export all reports and upload to Google Drive ===
def export_and_upload_students(library_id):
    students = Logics.view_database.view.get_students(library_id)
    books = Logics.view_database.view.get_books(library_id)
    bookstock = Logics.view_database.view.get_book_stock(library_id)
    passedout = Logics.view_database.view.get_passedout_students(library_id)
    borrowregister = Logics.view_database.view.get_borrowed_books(library_id)
    teacher = Logics.view_database.view.get_teachers(library_id)
    teacherissueregister = Logics.view_database.view.get_teacher_borrowed_books(library_id)
    cashbook = Logics.view_database.view.get_cash_transactions(library_id)
    # Export Excel files
    download_books_excel(books)
    download_students_excel(students)
    download_stocks_excel(bookstock)
    download_borrowed_books_excel(borrowregister)
    download_passedout_students_excel(passedout)
    download_teachers_excel(teacher)
    download_teacher_borrowed_books_excel(teacherissueregister)
    download_cashbook_excel(cashbook)
 
    # Upload them all
    return upload_exports_folder(library_id)
 
# === Optional background backup loop (e.g., daily auto-backup) ===
def backup(library_id):
    while True:
        try:
            export_and_upload_students(library_id)
        except Exception as e:
            msg = f"Backup failed:\n{str(e)}"
            print(msg)
        # time.sleep()  # Wait 1 day

def backuploop(library_id):
    try:
        export_and_upload_students(library_id)
    except Exception as e:
        print("Manual backup failed:\n{str(e)}")
        
def manual_backup(library_id):
    try:
        if export_and_upload_students(library_id):
            return True
        else:
            return False
    except Exception as e:
        print("Manual backup failed:\n{str(e)}")
# === Example: Trigger backup once ===
# manual_backup("394083")