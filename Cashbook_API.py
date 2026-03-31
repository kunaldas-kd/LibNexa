import os
import webview
import Withdrawal_API as WA
import Logics.view_database as view_database
import Logics.handle_menu as handle_menu
import Dashboard_API as dashboard_API

class CashBookAPI:
    """API for managing cash transactions in MySQL."""
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return self.user_id

    def fetch_Cashbook(self):
        """
        Fetch and return the list of cash transactions from MySQL.
        """
        id = self.get_id()
        try:
            transactions = view_database.view.get_cash_transactions(id)
            print(transactions)
            if not transactions:
                return []
            return [{
                "Sl_No" : row[0],
                "Transaction_ID": row[1],  # Unique transaction identifier
                "Student_ID": row[2],  # Associated student ID
                "Transaction_Date": row[3],  # Date of transaction
                "Description": row[4],  # Transaction details
                "Transaction_Type": row[5],  # Credit/Debit type
                "Amount": float(row[6]) if row[6] else 0.0,  # Transaction amount
                "Credit": row[7],
                "Debit": row[8],
                "Balance": float(row[9]) if row[9] else 0.0
            } for row in transactions]
        except Exception as e:
            print(f"Error fetching cash transactions: {e}")
            return []

    def download(self,Start_Date=None, End_Date=None):
        """
        Downloads cash transactions data as a CSV file.
        """
        id = self.get_id()
        res = handle_menu.download_cash_book(id,Start_Date, End_Date)
        return True if res else False

    def Debit(self):
        id = self.get_id()
        WA.open_debit_page(id)

    def go_back(self):
        """Closes the current webview window and opens the dashboard."""
        user = self.get_id()
        dashboard_API.open_dashboard(user)

def open_cashbook_dashboard(user_id):
    """
    Opens the Cash Book Dashboard in a webview window.
    """

    html_path = os.path.join(os.path.dirname(__file__), "LMS/templates/Cash_Book.html")
    # html_path = os.path.join(os.path.dirname(__file__), "templates/Cash_Book.html")
    if not os.path.exists(html_path):
        print("Error: Cashbook.html not found!")
        return

    with open(html_path, "r", encoding="utf-8") as file:
        html = file.read()

    api = CashBookAPI(user_id)
    webview.windows[0].load_html(html)
    webview.windows[0].expose(api.fetch_Cashbook)
    webview.windows[0].expose(api.download)
    webview.windows[0].expose(api.Debit)
    webview.windows[0].expose(api.go_back)
#     webview.create_window(
#                 "Payment Page",
#                 html=html,
#                 js_api=api,
#                 width=500,
#                 height=600
#                 # resizable=False
#             )
#     webview.start()
# # # Uncomment the following lines to test the API
# if __name__ == "__main__":
#     open_cashbook_dashboard("394083")  # Replace with actual user_id