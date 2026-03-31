import os
import webview
import Logics.Book_Recovery as BR
import Logics.Borrow_Register as Borrow_Register
import Teacher_Register_API as dashboard_API
import Logics.CHECK_INTERNET as CHECK_INTERNET

class BookIssueRegisterAPI:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return self.user_id
    
    def getteacherdetails(self, teacherID):
        if not self.user_id or not teacherID:
            return {"status": "error", "message": "Missing Teacher ID."}
        user_db = f"{self.user_id}_library_db"
        try:
            getdetails = Borrow_Register.get_teacher_details(user_db, teacherID)
            print(getdetails)
            if getdetails:
                return {"status": "success", "Teacher_Name": getdetails["Teacher_Name"], "Designation": getdetails["Designation"], "Department": getdetails["Department"]}
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

    def issue_book_to_teacher(self, borrowDetails):
        """
        Issues a book to a teacher after validating all required conditions.
        """
        print("Issuing book with details:", borrowDetails)
        Id = self.get_id()
        result = CHECK_INTERNET.is_connected()
        if result == False:
            return {"check_internet": False}
        else:
            if not Id or not borrowDetails:
                return {"status": "error", "message": "Missing user ID or book issue details."}

            if Borrow_Register.valid_Teachers(Id, borrowDetails) == False:
                return {"status": "error", "reason": "Invalid_Teacher"}

            if Borrow_Register.valid_Books(Id, borrowDetails)== False:
                return {"status": "error", "reason": "Invalid_Book"}

            if Borrow_Register.valid_BOOKinstock(Id, borrowDetails) == False:
                return {"status": "error", "reason": "Out_of_Stock"}

            # Insert into register
            res = Borrow_Register.insert_into_teacher_borrow_register(Id, borrowDetails)
            if res == True:
                return True
            elif isinstance(res, dict) and res.get("ex") is False:
                return {"EX": False, "massage": "He is not working in this institute anymore."}
            else:
                return False

    def go_back(self):
        user = self.get_id()
        dashboard_API.open_teacher_borrow_dashboard(user)

def open_book_issue_page_for_teachers(user_id):
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/Book_issue_for_teacher.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/Book_issue_for_teacher.html")
    if not os.path.exists(TEMPLATE_PATH):
        print("Error: Book_issue_for_teacher.html not found at:", TEMPLATE_PATH)
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        book_issue_html = file.read()

    api = BookIssueRegisterAPI(user_id)
    webview.windows[0].load_html(book_issue_html)
    webview.windows[0].expose(api.get_book_details)
    webview.windows[0].expose(api.getteacherdetails)
    webview.windows[0].expose(api.issue_book_to_teacher)
    webview.windows[0].expose(api.go_back)
#     teacher_window = webview.create_window(
#         "Issue Book - Teacher Panel",
#         html=book_issue_html,
#         js_api=api,
#         width=1100,
#         height=720,
#         resizable=True
#     )
#     webview.start()

# # Entry point
# if __name__ == "__main__":
#     open_book_issue_page_for_teachers("877509")  # Replace with dynamic ID if needed
