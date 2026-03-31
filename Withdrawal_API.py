import os
import webview
import Logics.database_connector as database_connector
import Logics.fund as fund
import Cashbook_API

class DebitAPI:
    def __init__(self, id):
        self.user_id = id

    def get_id(self):
        return self.user_id

    def debit_amount(self, member_type, member_name, amount, reason):
        Id = self.get_id()
        if not Id or not member_type or not member_name or not amount or not reason:
            return "Error: Missing required fields."

        user_db_name = f"{Id}_library_db"

        try:
            status = fund.Debit(user_db_name, member_type, member_name, float(amount), reason)
            return status
        except Exception as e:
            return f"Error during debit processing: {str(e)}"
        
    def go_back(self):
        """Closes the current webview window."""
        user = self.get_id()
        Cashbook_API.open_cashbook_dashboard(user)

def open_debit_page(user_id):
    
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/Debit_form.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/Debit_form.html")

    if not os.path.exists(TEMPLATE_PATH):
        print("Error: Debit.html not found!")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        debit_html = file.read()

    api = DebitAPI(user_id)

    try:
        webview.windows[0].load_html(debit_html)
        webview.windows[0].expose(api.debit_amount)
        webview.windows[0].expose(api.go_back)
        # webview.create_window(
        #     "Debit Page",
        #     html=debit_html,
        #     js_api=api,
        #     width=500,
        #     height=650,
        #     resizable=False
        # )
        # webview.start()
    except Exception as e:
        print(f"Failed to create a WebView2 window: {e}")

        



# if __name__ == "__main__":
#     open_debit_page("394083")