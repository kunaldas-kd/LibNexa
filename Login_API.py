import os
import webview
# from getmac import get_mac_address

import Logics.user_authentication as user_authentication
import Logics.store_mac_address as store_mac_address
import Forget_API as forget_api
import Main as main
# import backup
# import time

class LoginAPI:
    def login(self, username, password, save_password):
        """Handles user login and redirects to the dashboard upon success"""
        try:
            if not user_authentication.login_user(username, password):
                return False

            if save_password:
                store_mac_address.storemac(username)

            return True
        except Exception as e:
            print(f"Unexpected error during login: {e}")
            return "An unexpected error occurred."

    def go_back(self):
        """Closes the login window to return to the main page"""
        try:
            main.backtomain()
        except Exception as e:
            print(f"Error in go_back: {e}")

    def forget_password(self):
        """Opens the forget password page"""
        try:
            forget_api.open_forget_password()
        except Exception as e:
            print(f"Error in forget_password: {e}")


def open_login():
    """Opens the Login Page or auto signs in if MAC address exists"""
    # mac = get_mac_address()
    # print(f"Detected MAC Address: {mac}")

    credentials = store_mac_address.autosignin()
    print(f"Auto-signin credentials: {credentials}")

    if credentials and isinstance(credentials, tuple) and len(credentials) == 2:
        user_id, password = credentials
        if user_authentication.login_user(user_id, password):
            print("Auto-login successful.")
            return True
        else:
            print("Auto-login failed. Incorrect credentials.")
    else:
        print(" MAC not registered or auto-login not available.")

    # Manual login fallback
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/login.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/login.html")
    if not os.path.exists(TEMPLATE_PATH):
        print("❌ Login template not found.")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        login_html = file.read()

    api = LoginAPI()
    window = webview.windows[0]
    window.load_html(login_html)
    window.expose(api.login)
    window.expose(api.go_back)
    window.expose(api.forget_password)
#     window = webview.create_window("Login", html=login_html, js_api=api)
#     webview.start()


# if __name__ == "__main__":
#     open_login()

        

      