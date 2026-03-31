import Dashboard_API
import time
import os
import webview
from Logics import database_connector
import Logics.password_generator as otp
import Logics.settings as settings
import Logics.store_mac_address
import Main
import random
import Logics.send_email as email
import backupdownload
import Logics.CHECK_INTERNET as check_internet
import backup
import base64

class SettingsAPI:
    def __init__(self, Id):
        self.user_id = Id
        self.pending_settings = {}
        self.generated_otp = None
        self.otp_timestamp = None

    def get_id(self):
        return self.user_id

    def enabling_the_payment_function(self, enable, entered_otp=0):
        user_db_name = f"{self.user_id}_library_db"
        conn = database_connector.connect_to_db(user_db_name)
        cursor = conn.cursor()

        print(f"[DEBUG] Payment toggle requested: {'Enable' if enable else 'Disable'}, OTP: {entered_otp}")

        if enable:
            # === OTP Flow for Enabling ===
            if not entered_otp:
                self.generated_otp = ''.join(str(random.randint(0, 9)) for _ in range(6))
                self.otp_timestamp = time.time()
                cursor.execute("SELECT Library_name, Institute_Email FROM users")
                name, Email = cursor.fetchone()
                email.send_otp_email(Email, name, self.generated_otp)
                print(f"🔐 OTP for enabling payment (User {self.user_id}): {self.generated_otp}")
                return {"status": "otp_sent"}

            if not self.generated_otp or time.time() - self.otp_timestamp > 300:
                self.generated_otp = None
                self.otp_timestamp = None
                return {"status": "expired"}

            if entered_otp != self.generated_otp:
                return {"status": "invalid"}

            # OTP verified
            self.generated_otp = None
            self.otp_timestamp = None

        # No OTP needed for disable, or OTP verified
        result = settings.Payment_Function(conn, enable)
        print(f"[DEBUG] settings.Payment_Function() result: {result}")
        return result == 1 or result is True

    def fetch_payment_settings(self):
        user_db_name = f"{self.user_id}_library_db"
        conn = database_connector.connect_to_db(user_db_name)
        res = settings.fetchstatus(conn)
        print(res)
        latefine, period, books, payment= res
        return {"late fine" : float(latefine), "borrow period": int(period), "number of books": int(books), "payment status": payment}

    def stage_settings(self):
        self.generated_otp = ''.join(str(random.randint(0, 9)) for _ in range(6))
        self.otp_timestamp = time.time()
        user_db_name = f"{self.user_id}_library_db"
        conn = database_connector.connect_to_db(user_db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT Library_name, Institute_Email FROM users")
        name, Email = cursor.fetchone()
        email.send_otp_email(Email, name, self.generated_otp)
        print(f"🔐 OTP for user {self.user_id}: {self.generated_otp}")
        return True

    def verify_otp(self, entered_otp, books, fine, period):
        if not self.generated_otp or time.time() - self.otp_timestamp > 300:
            self.generated_otp = None
            self.otp_timestamp = None
            return {"status": "expired"}

        if entered_otp == self.generated_otp:
            user_db_name = f"{self.user_id}_library_db"
            conn = database_connector.connect_to_db(user_db_name)
            res = settings.run(conn, books, fine, period)
            self.generated_otp = None
            self.otp_timestamp = None
            return res is True
        else:
            return {"status": "invalid"}

    def stage_settings_resend(self):
        if not self.generated_otp:
            return False

        self.generated_otp = ''.join(str(random.randint(0, 9)) for _ in range(6))
        self.otp_timestamp = time.time()
        user_db_name = f"{self.user_id}_library_db"
        conn = database_connector.connect_to_db(user_db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT Library_name, Institute_Email FROM users")
        name, Email = cursor.fetchone()
        email.send_otp_email(Email, name, self.generated_otp)
        print(f"🔄 Resent OTP for user {self.user_id}: {self.generated_otp}")
        return True

    def logout(self):
        Logics.store_mac_address.clearmac(self.user_id)
        Main.backtomain()

    def go_back(self):
        print("[DEBUG] Navigating back to settings.")
        Dashboard_API.open_dashboard(self.user_id)

    def initiate_backup(self):
        if not check_internet.is_connected():
            return{"check_internet": False}
        
        elif backupdownload.download_all_files_to_libnest_backup(self.get_id()) == True:
            print("yes")
            return True
        else:
            return False 

    def initiate_manual_backup(self):
        if not check_internet.is_connected():
            return{"check_internet": False}
        
        elif backup.manual_backup(self.get_id()) == True:
            print("yes")
            return True
        else:
            return False


def load_image_as_base64(image_filename):
    """
    Helper function to load image as base64 data URL
    
    Args:
        image_filename (str): Name of the image file in templates folder
    
    Returns:
        str: Base64 data URL or empty string if file not found
    """
    image_path = os.path.join(os.path.dirname(__file__), f"LMS/templates/{image_filename}")
    
    try:
        with open(image_path, "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        return f"data:image/png;base64,{image_base64}"
    except FileNotFoundError:
        print(f"❌ Warning: {image_filename} not found!")
        return ""
    except Exception as e:
        print(f"❌ Error loading {image_filename}: {str(e)}")
        return ""

def open_settings(user_id):
    # Check if template exists
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/Setting.html")
    if not os.path.exists(TEMPLATE_PATH):
        print("❌ Error: Setting.html not found!")
        return

    try:
        # Load both images
        logout_logo = load_image_as_base64("logout.png")
        restore_logo = load_image_as_base64("restore.png")

        # Read template
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
            page_html = file.read()

        # Replace all image placeholders
        replacements = {
            "{{logo_path}}": logout_logo,           # For logout button
            "{{restore_logo}}": restore_logo,       # For restore button
            "{{logout_logo}}": logout_logo          # Alternative placeholder name
        }
        
        for placeholder, image_data in replacements.items():
            page_html = page_html.replace(placeholder, image_data)

        # Initialize API
        api = SettingsAPI(user_id)
        webview.windows[0].load_html(page_html)
        webview.windows[0].expose(api.enabling_the_payment_function)
        webview.windows[0].expose(api.fetch_payment_settings)
        webview.windows[0].expose(api.stage_settings)
        webview.windows[0].expose(api.stage_settings_resend)
        webview.windows[0].expose(api.verify_otp)
        webview.windows[0].expose(api.go_back)
        webview.windows[0].expose(api.logout)
        webview.windows[0].expose(api.initiate_backup)
        # webview.windows[0].expose(api.initiate_manual_backup)
        # Create webview window
#         global_window = webview.create_window(
#             "Library Management System",
#             html=page_html,
#             js_api=api,
#             fullscreen=False,
#             width=1200,      # Optional: set window dimensions
#             height=800,      # Optional: set window dimensions
#             resizable=True   # Optional: make window resizable
#         )

#         # Start webview
#         webview.start()
        
    except Exception as e:
        print(f"❌ Error opening settings: {str(e)}")
        return
    
# if __name__ == "__main__":
#     open_settings("394083")