import os
import webview

import Logics.forgotpassword as forgotpassword
import Login_API as login_API

class ForgetPasswordAPI:
    def recover_password(self, user_input):
        print(user_input)
        """Handles password recovery for User ID or Email ID"""
        if not user_input:
            return "User ID or Email ID is required!"

        if '@' in user_input:  # If input contains '@', assume it's an Email ID
            try:
                res = forgotpassword.forgot_password2(user_input)
                print(res)
                if res==True:
                    login_API.open_login()
                    # webview.windows[0].destroy()
                    return True
                else:
                    return False
            except Exception as e:
                # logging.error(f"Error processing email input: {e}")
                return "Error processing password recovery for Email ID."
           
        else:  
            try:
                
                res = forgotpassword.forgot_password(user_input)
                print(res)
            
                if res==True:
                    login_API.open_login()
                    # webview.windows[0].destroy()
                    return True
                else:
                    return False
            except Exception as e:
                # logging.error(f"Error processing user ID input: {e}")
                return "Error processing password recovery for User ID."
    def go_back(self):
        """Closes the login window to return to the main page"""
        login_API.open_login()
        # webview.windows[0].destroy()   
                

   
        

def open_forget_password():
    """Opens the Forget Password Page"""
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/forget_pass.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/forget_pass.html")
    if not os.path.exists(TEMPLATE_PATH):
        print("Error: forget_password.html not found in templates folder!")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        forget_password_html = file.read()

    webview.windows[0].load_html(forget_password_html)

    
    api = ForgetPasswordAPI()
    webview.windows[0].expose(api.recover_password)
    webview.windows[0].expose(api.go_back)
   
#     window = webview.create_window(
#         "Forget Password Page",
#         html=forget_password_html,
#         js_api=ForgetPasswordAPI(),width= 1000,
#         height= 600,
#         fullscreen=False
#     )
#     # window.maximize()
# if __name__ == "__main__":
#     open_forget_password()
#     webview.start()