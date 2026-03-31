import os
import time
import threading
import webview
import Register_API as register_API
import Login_API as login_API
import builtins
import base64
import Logics.CHECK_INTERNET as CHECK_INTERNET

class API:
    def open_login(self):
        
        result = CHECK_INTERNET.is_connected()
        if result == False:
            return {"check_internet": False}
        elif result == True:
            login_API.open_login()
            
        else:
            return {"error":False}

    def open_register(self):
        result = CHECK_INTERNET.is_connected()
        if result == False:
            return {"check_internet": False}
        else:
            register_API.open_register()
            return {"check_internet": True}

def open_main():
    """Loads the main window after splash"""
    builtins.print = lambda *args, **kwargs: None
    time.sleep(5)
    # webview.windows[0].toggle_fullscreen()
     
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/main.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/main.html")
    

    if not os.path.exists(TEMPLATE_PATH):
        print("Error: main.html not found in templates folder!")
        return
    logo_path = os.path.join(os.path.dirname(__file__), "LMS/templates/logo1.png")
    # logo_path = os.path.join(os.path.dirname(__file__), "templates/logo1.png")
    with open(logo_path, "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    logo_data_url = f"data:image/png;base64,{logo_base64}"

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        main_html = file.read()

    main_html = main_html.replace("{{logo_path}}", logo_data_url)

    api = API()
    webview.windows[0].load_html(main_html)
    webview.windows[0].expose(api.open_login)
    webview.windows[0].expose(api.open_register)

def backtomain():
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/main.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/main.html")
    

    if not os.path.exists(TEMPLATE_PATH):
        print("Error: main.html not found in templates folder!")
        return
    logo_path = os.path.join(os.path.dirname(__file__), "LMS/templates/logo1.png")
    # logo_path = os.path.join(os.path.dirname(__file__), "templates/logo1.png")

    with open(logo_path, "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    logo_data_url = f"data:image/png;base64,{logo_base64}"

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        main_html = file.read()

    main_html = main_html.replace("{{logo_path}}", logo_data_url)

    api = API()
    webview.windows[0].load_html(main_html)
    webview.windows[0].expose(api.open_login)
    webview.windows[0].expose(api.open_register)

def open_splash():
    # builtins.print = lambda *args, **kwargs: None
    """Opens splash screen and starts main window after delay"""
    splash_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'LMS/templates/splash.html')
    # splash_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/splash.html')
    splash_url = 'file://' + splash_path.replace('\\', '/')

    if not os.path.exists(splash_path):
        print(f"Error: splash.html not found at {splash_path}")
        return

    # Create the splash window
    webview.create_window('LibNexa', splash_url, width=1000, height=600)
    threading.Thread(target=open_main, daemon=True).start()
    webview.start(gui='edgechromium')
    
if __name__ == "__main__":
    open_splash()


