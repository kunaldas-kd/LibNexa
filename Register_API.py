import os
import webview
import Logics.registration as registration
import Logics.EMAIL_EXISTANCE as EMAIL_EXISTANCE
import Logics.validation as validation
import Main as main
import Logics.CHECK_INTERNET as CHECK_INTERNET
import Logics.database_setup as database_setup
# global_window = None
class API:
    def go_back(self):
        """Closes the login window to return to the main page"""
        main.backtomain()
        # webview.windows[0].destroy()
    def submit_registration(self, data):
        """Handles registration data from the frontend and calls backend functions."""
        # Call your backend logic to insert the registration data

        database_setup.setup_admin_interface_database()
        result = CHECK_INTERNET.is_connected()
        if result == False:
            return {"check_internet": False}
        
        email_upper = data.get("instituteEmail", "").upper().strip()
        response = validation.Valid.verify_email(email_upper)
        # print(response)
        if response == False:
            return {"valid_email": False}
        response1 = EMAIL_EXISTANCE.get_institutional_emails(email_upper)
        # print(response1)
        if response1 == False:
            return {"is_valid": False}
        else:
            user_id = registration.insert_library_info(data)
            status = user_id
            print(status)
            if status == True:
                
                print("Registration successful")
                return {"Status":True}  # Return success message
            else:
                print("Registration failed.")
                return "Registration failed. Please try again."  # Return failure message

# def open_register(global_window):
def open_register():
    """Opens the Register Window"""
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/register.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/register.html")
    if not os.path.exists(TEMPLATE_PATH):
        print("Error: login.html not found in templates folder!")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        register_html = file.read()
    

    
    api = API()
    webview.windows[0].load_html(register_html)
    webview.windows[0].expose(api.submit_registration)
    webview.windows[0].expose(api.go_back)
    
#     window = webview.create_window("Register Page", html=register_html, 
#                         #   width=500, height=600, 
#                           js_api=API(),
#                           width= 1000,
#                           height= 600,
#                           fullscreen=False
#                           )
#     # def maximize_window():
#         # """Maximizes the window after it has fully loaded"""
#     # window.maximize()
#     webview.start()

# if __name__ == "__main__":
#     open_register()
