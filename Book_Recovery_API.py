import os
import webview
import Logics.Book_Recovery as BR
from Logics.total_amount_taking import fatch_book_price , fatch_book_price
from Logics.Book_Recovery import Confirm_Book
import Dashboard_API
from Logics.fund import Credit
class RecoveryAPI:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        """
        Returns the current user's ID.
        """
        return self.user_id

    def go_back(self):
        """
        Returns to the dashboard.
        """
        Dashboard_API.open_dashboard(self.user_id)

    def get_amount(self, book_id):
        """
        Returns the total outstanding amount for the given student.
        """
        if not self.user_id or not book_id:
            return {"status": "error", "message": "Missing Student ID."}

        user_db = f"{self.user_id}_library_db"
        try:
            total = fatch_book_price(user_db, book_id)
            if total > 0:
                return {"status": "success", "amount": total}
            else:
                return {"status": "error", "message": "No outstanding amount found."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    def get_book_details(self, bookID):
        if not self.user_id or not bookID:
            return {"status": "error", "message": "Missing Student ID."}
        user_db = f"{self.user_id}_library_db"
        try:
            getdetails = BR.getbookdetails(user_db, bookID)
            print(getdetails)
            if getdetails:
                return {"status": "success", "bookname": getdetails["bookname"], "author": getdetails["author"], "Published_Year": getdetails["Published_Year"], "Edition": getdetails["Edition"],"Price": getdetails["Price"]}
            else:
                return {"status": "error", "message": "No outstanding details found."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        

    def confirm_book_recovery(self, bookID, publishedYear, edition, bookPrice):
        """
        Confirms book recovery and logs it in the database.
        """
        if not all([bookID,publishedYear, edition, bookPrice]):
            return {"status": "error", "message": "Missing Book ID."}
        print(bookID, edition, bookPrice)
        try:
            user_db = f"{self.user_id}_library_db"
            result = Confirm_Book(user_db, bookID, publishedYear, edition, bookPrice)
            if result:
                return {"status": "success", "message": "✔️ Book recovery confirmed."}
            else:
                return {"status": "success", "message": "❌ No update is needed. Just keep the new book and assign it to the previous Book ID."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def confirm_cash_recovery(self, student_id, book_id, newamount, paymentType, reason):
        """
        Confirms cash recovery and logs it in the database.
        """
        if not all([student_id, book_id, newamount, paymentType, reason]):
            return {"status": "error", "message": "All fields are required for cash recovery."}

        try:
        
            user_db = f"{self.user_id}_library_db"
            received = newamount
            result = Credit(user_db, student_id, book_id, received, paymentType, reason)
            if result:
                return {"status": "success", "message": "✅ Cash recovery confirmed."}
            else:
                return {"status": "success", "message": "❌ Cash recovery confirmed."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

def open_recovery_page(user_id):
    """
    Opens the ConfirmRecovery page and exposes RecoveryAPI methods to frontend.
    """
    template_path = os.path.join(os.path.dirname(__file__), "LMS/templates/Confirm_Book_or_Cash_Recovery.html")
    # template_path = os.path.join(os.path.dirname(__file__), "templates/Confirm_Book_or_Cash_Recovery.html")

    if not os.path.exists(template_path):
        print("❌ Recovery page not found.")
        return

    with open(template_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    api = RecoveryAPI(user_id)

    try:
        webview.windows[0].load_html(html_content)
        webview.windows[0].expose(api.go_back)
        webview.windows[0].expose(api.get_amount)
        webview.windows[0].expose(api.get_book_details)
        webview.windows[0].expose(api.confirm_book_recovery)
        webview.windows[0].expose(api.confirm_cash_recovery)
    except Exception as e:
        print(f"❌ Failed to load recovery page: {e}")

    # webview.create_window(
    #             "Debit Page",
    #             html=html_content,
    #             js_api=api,
    #             width=500,
    #             height=650                
    #         )
    # webview.start()



# if __name__ == "__main__":
#     open_recovery_page("163452")