import os
import webview
import Logics.database_connector as database_connector  # Module for establishing the database connection.
import Logics.Borrow_Register as Borrow_Register
import View_Borrow_Register_API as dashboard_API
import Logics.Book_Recovery as BR
import Logics.CHECK_INTERNET as CHECK_INTERNET

class BookIssueRegisterAPI:
    def __init__(self, id):
        self.user_id = id  # Store the user ID for reuse.

    def get_id(self):
        return self.user_id
    
    def get_student_details(self, studentID):
        if not self.user_id or not studentID:
            return {"status": "error", "message": "Missing Student ID."}
        user_db = f"{self.user_id}_library_db"
        try:
            getdetails = Borrow_Register.getstudentdetails(user_db, studentID)
            print(getdetails)
            if getdetails:
                return {"status": "success", "studentname": getdetails["studentname"], "Department": getdetails["Department"], "admissionyear": getdetails["admissionyear"]}
            else:
                return {"status": "error", "message": "No outstanding details found."}
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
                return {"status": "success", "bookname": getdetails["bookname"], "author": getdetails["author"], "Published_Year": getdetails["Published_Year"], "Price": getdetails["Price"]}
            else:
                return {"status": "error", "message": "No outstanding details found."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    def issue_book_to_student(self, borrowDetails):
        """
        Issues a book to a student.
        """
        print(borrowDetails)
        Id = self.get_id()
        if not Id or not borrowDetails:
            return {"status": "error", "message": "Missing 'Id', 'student_id', or 'book_id' parameters!"}
        
        result = CHECK_INTERNET.is_connected()
        if result == False:
            return {"check_internet": False}
        else:
            res = Borrow_Register.valid_Students(Id, borrowDetails)
            if res == False:
                return {"Invalid_Student": False}
            res0 = Borrow_Register.valid_Books(Id, borrowDetails)
            if res0 == False:
                return {"Invalid_Book": False}
            res1 = Borrow_Register.valid_payment(Id, borrowDetails)
            if res1 == False:
                return {"Payment": False}
            res2 = Borrow_Register.valid_limiting_book(Id, borrowDetails)    
            if res2 == False:
                return {"Limiting_book": False}
            res3 = Borrow_Register.valid_BOOKinstock(Id, borrowDetails)
            if res3 == False:
                return {"Stock_book": False}
            else:
                issue_status = Borrow_Register.insert_into_borrow_register(Id, borrowDetails)
                print(issue_status)
                if issue_status.get("done") == True:
                    return {"done" : True}
                elif issue_status.get("email") == False:
                    return {"email" : False}
                elif issue_status.get("block") == False:
                    return {"block" : False}
                else:
                    return False

    def go_back(self):
        """Closes the current webview window."""
        user = self.get_id()
        dashboard_API.open_borrow_register_dashboard(user)

def open_book_issue_page(user_id):
    """
    Opens the Book Issue Page using pywebview.
    Loads the HTML template and calls the above API methods.
    """
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/Book_issue.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/Book_issue.html")

    if not os.path.exists(TEMPLATE_PATH):
        print("Error: book_issue.html not found!")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        book_issue_html = file.read()

    api = BookIssueRegisterAPI(user_id)

    webview.windows[0].load_html(book_issue_html)
    webview.windows[0].expose(api.go_back)
    webview.windows[0].expose(api.issue_book_to_student)
    webview.windows[0].expose(api.get_book_details)
    webview.windows[0].expose(api.get_student_details)

#     global_window = webview.create_window(
#         "Library Management System",
#         html=book_issue_html,
#         js_api=api,
#         fullscreen=False  
#     )
#     webview.start()
# if __name__ == "__main__":
#     open_book_issue_page("394083")  