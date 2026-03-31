import os
import webview
import Logics.database_connector as database_connector
import Logics.view_database as view_database
import Logics.missingbook as issueresister
import Logics.handle_menu as handle_menu
import Dashboard_API as dashboard_API
import Book_issue_register_API as Book_issue_register_API
from Logics.payment import payment  # Custom module for handling payment workflows.
from Logics.total_amount_taking import fatch_amount_1
import Logics.Borrow_Register as validpayment
import Logics.transaction as renew
import Logics.transaction as transaction
import Logics.Borrow_Register as valided_payment
import Logics.CHECK_INTERNET as CHECK_INTERNET
class BorrowRegisterAPI:
    """API for retrieving borrow register data from MySQL."""
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return self.user_id

    def fetchborrowregister(self):
        """
        Fetch and return the borrow register list from MySQL.
        """
        id = self.get_id()
        try:
            borrow_list = view_database.view.get_borrowed_books(id)
            if not borrow_list:
                return []
            return [{
                "Sl_No": row[0],
                "Book_ID": row[1],
                "Student_ID": row[2],
                "Student_Name": row[3],
                "Student_Email": row[4],
                "Department": row[5],
                "Book_Name": row[6],
                "Author": row[7],
                "Published_Year": row[8],
                "Edition": row[9],
                "Book_Price": row[10],
                "Borrow_Date": row[11].isoformat() if row[11] else "",
                "Return_Date": row[12].isoformat() if row[12] else "",
                "Payable_Amount": float(row[13]) if row[13] else 0.0,
                "Borrow": row[14],
                "Submit": row[15],
                "Renew": row[16],
                "Payment_Status": row[17],
                "Reminder": row[18]
            } for row in borrow_list]
        except Exception as e:
            print(f"Error fetching borrow register: {e}")
            return []

    def download(self, start_date=None, end_date=None):
        """
        Downloads the borrowed books report.
        If no date range is provided, downloads all records.
        """
        id = self.get_id()

        # If date range provided, pass it to your download logic
        if start_date and end_date:
            res = handle_menu.download_borrowed_books(id, start_date, end_date)
            if res == True:
                # print (res)
                return True
            else:
                return False
        else:
            res = handle_menu.download_borrowed_books(id,start_date, end_date)
            if res == True:
                # print (res)
                return True
            else:
                return False

    def total_issued(self):
        """Closes the login window to return to the main page"""
        id = self.get_id()
        result = issueresister.Total_Issued(id)
        issued, total,  Submit, renew = result
        print(result)
        if result:
            return {
                "total":total,
                "issue":issued,
                "submit":Submit,
                "renew":renew
            }
        else:
            return {
                "total":0,
                "issued":0,
                "submit":0,
                "renew":0
            }
        
    def issue_book(self):
        """Issues a book to a student."""
        id = self.get_id()
        Book_issue_register_API.open_book_issue_page(id)
            
    def renew_book(self, renewBookData):
        """Renews a book in the database."""
        user_id = self.get_id() 
        db = f"{user_id}_library_db"
        try:
            result = CHECK_INTERNET.is_connected()
            if result == False:
                return {"check_internet": False}
            else:
                valid_payment = validpayment.valid_payment(user_id, renewBookData)
                print(valid_payment)
                if not valid_payment:
                    # Start a separate thread for payment handling
                    # payment_thread = threading.Thread(target=payment_API.open_payment_page, args=(user_id,), daemon=True)
                    # payment_thread.start()
                    return {"payment": False}

                else:
                    # Directly renew the book if payment is valid
                    renewal_status = renew.renew_book(db, renewBookData)
                    if renewal_status == True:
                        return {"Renewed": True}
                    else:
                        return {"Renewed": False}
                 
        except Exception as e:
            print(f"Failed to renew book: {e}")
            return False
        
    def submit_book(self, submitbook):
        """Marks a book as returned in the database."""
        Id = self.get_id()
        try:
            result = CHECK_INTERNET.is_connected()
            if result == False:
                return {"check_internet": False}
            else:
                res = valided_payment.valid_payment(Id, submitbook)
                
                if res == False:
                    
                    submit = transaction.submit_book(Id, submitbook)
                    if submit == True:
                        return {"success":True}
                    else:
                        return False
                else:
                    submit = transaction.submit_book(Id, submitbook)
                    if submit.get("done") == True:
                        return True
                    elif submit.get("email") == False:
                        return {"email" : False}
                    else:
                        return False
                
        except Exception as e:
            print(f"Failed to submit book: {e}")

    def process_payment(self, student_id):
        """
        Processes payment using the payment function directly.
        """
        print(student_id)
        Id = self.get_id()
        if not Id or not student_id:
            return "Error: Missing 'Id' or 'student_data' parameters!"

        # Construct a user-specific database name.
        user_db_name = f"{Id}_library_db"
        

        try:
            result = CHECK_INTERNET.is_connected()
            if result == False:
                return {"check_internet": False}
            else:
                # Call the payment function directly
                payment_status = payment(user_db_name, student_id)
                if payment_status == True:
                    return True
                
                # elif payment_status == False:
                    
                else:
                    return False
        except Exception as e:
            return f"Error during payment processing: {str(e)}"
            
    def go_back(self):
        """Closes the current webview window."""
        user = self.get_id()
        dashboard_API.open_dashboard(user)
        # webview.windows[0].destroy()

def open_borrow_register_dashboard(user_id):
    """
    Opens the Borrow Register Dashboard in a webview window.
    """
    db_name = f"{user_id}_library_db"
    connection = database_connector.connect_to_db(db_name)
    cursor = connection.cursor()
    if connection:
        cursor.execute("SELECT `Payment Functionality` FROM users")
        result = cursor.fetchone()[0]
        if result == 1:
            html_path = os.path.join(os.path.dirname(__file__), "LMS/templates/Borrow_register_database.html")
            # html_path = os.path.join(os.path.dirname(__file__), "templates/Borrow_register_database.html")
            if not os.path.exists(html_path):
                print("Error: borrow_register.html not found!")
                return

            with open(html_path, "r", encoding="utf-8") as file:
                dashboard_html = file.read()

            api=BorrowRegisterAPI(user_id)
            webview.windows[0].load_html(dashboard_html)
            webview.windows[0].expose(api.fetchborrowregister)
            webview.windows[0].expose(api.total_issued)
            webview.windows[0].expose(api.download)
            webview.windows[0].expose(api.issue_book)
            webview.windows[0].expose(api.submit_book)
            webview.windows[0].expose(api.renew_book)
            webview.windows[0].expose(api.process_payment)
            webview.windows[0].expose(api.go_back)
        else:
            html_path = os.path.join(os.path.dirname(__file__), "LMS/templates/Borrow_register_2nd_page.html")
            # html_path = os.path.join(os.path.dirname(__file__), "templates/Borrow_register_2nd_page.html")
            if not os.path.exists(html_path):
                print("Error: borrow_register.html not found!")
                return

            with open(html_path, "r", encoding="utf-8") as file:
                dashboard_html = file.read()

            api=BorrowRegisterAPI(user_id)
            webview.windows[0].load_html(dashboard_html)
            webview.windows[0].expose(api.fetchborrowregister)
            webview.windows[0].expose(api.download)
            webview.windows[0].expose(api.total_issued)
            webview.windows[0].expose(api.issue_book)
            webview.windows[0].expose(api.submit_book)
            webview.windows[0].expose(api.renew_book)
            webview.windows[0].expose(api.go_back)
        
        
#     global_window = webview.create_window(
#         "Library Management System",
#         html=dashboard_html,
#         js_api=api,
#         fullscreen=False  
#     )
#     webview.start()
# if __name__ == "__main__":
#     open_borrow_register_dashboard("394083") 