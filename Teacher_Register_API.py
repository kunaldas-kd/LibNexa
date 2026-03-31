import os
import webview
import Logics.database_connector as database_connector
import Logics.view_database as view_database
import Logics.missingbook as issueresister
import Logics.handle_menu as handle_menu
import Dashboard_API as dashboard_API
import Teacher_book_issue as Book_issue_register_API
# import Teacher_book_submit as Submit_API
import Logics.Borrow_Register as Borrow_Register
import Logics.transaction as transaction

class TeacherBorrowRegisterAPI:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return self.user_id

    def fetchteacherborrowregister(self):
        id = self.get_id()
        try:
            borrow_list = view_database.view.get_teacher_borrowed_books(id)
            if not borrow_list:
                return []
            return [
                {
                    "Sl_No": row[0],
                    "Book_ID": row[1],
                    "Teacher_ID": row[2],
                    "Teacher_Name": row[3],
                    "Department": row[4],
                    "Book_Name": row[5],
                    "Author": row[6],
                    "Published_Year": row[7],
                    "Edition": row[8],
                    "Book_Price": row[9],
                    "Borrow_Date": row[10].isoformat() if row[10] else "",
                    "Borrow": row[11],
                    "Submit": row[12]
                }
                for row in borrow_list
            ]
        except Exception as e:
            print("Error fetching teacher borrow register:", e)
            return []

    def download(self,start_date=None, end_date=None):
        id = self.get_id()
        res = handle_menu.teacher_borrowed_books(id,start_date, end_date)
        return res is True

    def total_teacher_issued(self):
        id = self.get_id()
        try:
            issued, total, submit = issueresister.Total_Teacher_Issued(id)
            return {
                "total": total,
                "issue": issued,
                "submit": submit
            }
        except Exception as e:
            print("Error fetching teacher issue summary:", e)
            return {
                "total": 0,
                "issue": 0,
                "submit": 0
            }

    def issue_teacher_book(self):
        Book_issue_register_API.open_book_issue_page_for_teachers(self.user_id)

    def submit_teacher_book(self, submitbook):
        """Marks a book as returned by a teacher in the database."""
        Id = self.get_id()
        try:
            if not Id or not submitbook:
                return {"status": "error", "reason": "Missing user ID or book issue details."}

            if not Borrow_Register.valid_Books(Id, submitbook):
                return {"status": "error", "reason": "Invalid Book"}
            
            if not Borrow_Register.valid_Teachers(Id, submitbook):
                return {"status": "error", "reason": "Invalid Teacher"}
            
            else:
                submit = transaction.submit_book_teacher(Id, submitbook)  # Call teacher-specific submit function
                if submit:
                    return {"success": True}
                else:
                    return {"success": False}
        except Exception as e:
            print(f"Failed to submit book (teacher): {e}")
    def go_back(self):
        dashboard_API.open_dashboard(self.user_id)

def open_teacher_borrow_dashboard(user_id):
    html_path = os.path.join(os.path.dirname(__file__), "LMS/templates/Teacher_Register.html")
    # html_path = os.path.join(os.path.dirname(__file__), "templates/Teacher_Register.html")
    if not os.path.exists(html_path):
        print("Error: Teacher_Borrow_register.html not found!")
        return

    with open(html_path, "r", encoding="utf-8") as file:
        dashboard_html = file.read()

    api = TeacherBorrowRegisterAPI(user_id)

    # if not webview.windows:
    #     window = webview.create_window("Teacher Borrow Register", html=dashboard_html, js_api=api)
    #     webview.start()
    # else:
    window = webview.windows[0]
    window.load_html(dashboard_html)
    window.expose(api.fetchteacherborrowregister)
    window.expose(api.total_teacher_issued)
    window.expose(api.download)
    window.expose(api.issue_teacher_book)
    window.expose(api.submit_teacher_book)
    window.expose(api.go_back)

# # # Example usage:
# if __name__ == "__main__":
#     open_teacher_borrow_dashboard("394083")
