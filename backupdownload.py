import os, shutil
import sys
import platform
import ctypes
import io
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
import Logics.database_connector as database_connector
from Logics.EXCEL_DATA_PROCESSOR import UniversalProcessor
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

# === Download a file from Google Drive ===
def download_file_from_drive(file_name, library_id, download_folder):
    """
    Download a file from Google Drive to the specified folder.

    :param file_name: Name of the file to be downloaded.
    :param library_id: ID of the library to fetch the user's email.
    :param download_folder: Folder path where the file should be saved.
    :return: File content in memory or local file path.
    """
    # Connect to the database to get user email
    db_name = f"{library_id}_library_db"
    connection = database_connector.connect_to_db(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT Institute_Email FROM users")  # Get user email from DB
    email = cursor.fetchone()[0]
    cursor.close()

    creds = get_drive_credentials(email)  # Use email for token
    service = build('drive', 'v3', credentials=creds)

    # Search for the file on Google Drive by name (optional, you can also search by ID)
    query = f"name = '{file_name}' and trashed = false"
    result = service.files().list(q=query, fields="files(id, name)").execute()
    files = result.get('files', [])

    if not files:
        raise FileNotFoundError(f"No file found with name: {file_name}")

    file_id = files[0]['id']

    # Prepare to download the file
    request = service.files().get_media(fileId=file_id)
    file_path = os.path.join(download_folder, file_name)  # Download to specified folder
    fh = io.FileIO(file_path, 'wb')  # Open the file in write-binary mode
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()  # Download in chunks
        print(f"Download {int(status.progress() * 100)}%.")

    print(f"File '{file_name}' downloaded successfully.")
    return file_path



# === Function to download all files to LibNest backup folder in Downloads ===
def download_all_files_to_libnest_backup(library_id):
    # Set the destination folder to the user's Downloads/LibNest backup folder
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads", "LibNest backup")
    os.makedirs(download_folder, exist_ok=True)  # Create if not exists
    ctypes.windll.kernel32.SetFileAttributesW(download_folder, 0x02)
    # List all files in Google Drive
    query = "trashed = false"  # Change this if you need specific filters (e.g., only certain types)
    service = build('drive', 'v3', credentials=get_drive_credentials(library_id))

    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    if not files:
        print("No files found.")
        return

    for file in files:
        print(f"Downloading {file['name']}...")
        download_file_from_drive(file['name'], library_id, download_folder)
        for fname in os.listdir(download_folder):
            file_path = os.path.join(download_folder, fname)
            if os.path.isfile(file_path) and fname.endswith(".xlsx"):
                UniversalProcessor.process_file(file_path, library_id)
        # STOCK.process_files_BACKUP(download_folder, library_id)
        for filename in os.listdir(download_folder):
            if filename.endswith(".xlsx"):
                file_path = os.path.join(download_folder, filename)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        print(f"Deleted Excel file: {filename}")
                    except Exception as e:
                        print(f"Error deleting {filename}: {e}")

    if os.path.exists(download_folder):
        try:
            shutil.rmtree(download_folder)
            print("Directory 'LibNest backup' deleted.")
        except Exception as e:
            print(f"Error deleting LibNest backup folder: {e}")
    else:
        print("No such file or directory named 'LibNest backup' in Downloads.")
        
    return True
# Example Usage:
# To download all files to the LibNest backup folder inside Downloads:
# download_all_files_to_libnest_backup("394083")
