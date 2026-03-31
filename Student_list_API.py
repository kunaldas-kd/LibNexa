import os
import webview
from Logics.Borrow_Register import valid_payment
import Logics.Library_clearence as Library_clearence
import Logics.view_database as view_database
import Logics.handle_menu as handle_menu
import Dashboard_API as dashboard_API
import Logics.missingbook as total_student
import Student_entry_API
import Logics.database_connector as database_connector
import Logics.CHECK_INTERNET as CHECK_INTERNET
class StudentAPI:
    """API for retrieving student data from MySQL."""
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return self.user_id

    def fetchstudents(self):
        """
        Fetch and return the list of students from MySQL.
        """
        id = self.get_id()
        try:
            student_list = view_database.view.get_students(id)
            if not student_list:
                return []
            return list({
                "Student_ID": student[0],
                "Student_Name": student[1],
                "Date_Of_Birth": student[2].isoformat(),
                "Department": student[3],
                "Student_Email": student[4],
                "Phone_Number": student[5],
                "Address": student[6],
                "Admission_Year": student[7]
            } for student in student_list)
        except Exception as e:
            print(f"Error fetching students: {e}")
            return []
        
    def download(self, dept = None, admission = None):
        id = self.get_id()
        print(dept)
        res = handle_menu.download_students(id, dept, admission)
        print (res)
        if res == True:
            # print (res)
            return True
        else:
            return False

    def total_student(self):
        """Closes the login window to return to the main page"""
        id = self.get_id()
        return total_student.Total_student(id)
        # webview.windows[0].destroy()

    def open_student_entry(self):
        """Opens the Student Entry page."""
        id = self.get_id()
        Student_entry_API.open_student_entry(id)
    
    def clear_student_library(self,student_id):
        Id = self.get_id()
        # Library_clearance_API.open_clearance_page(id)
        if not Id or not student_id:
            return {"status": "error", "message": "Missing user ID or student ID"}

        user_db_name = f"{Id}_library_db"

        try:
            result = CHECK_INTERNET.is_connected()
            if result == False:
                return {"check_internet": False}
            else:
                # 1. Check unpaid dues
                total_due = Library_clearence.valid_payment(user_db_name, student_id)
                if total_due == False:
                    connection = database_connector.connect_to_db(user_db_name)
                    if connection is None:
                        print("Failed to connect to the database.")
                        return  # Use buffered cursor
                    cursor = connection.cursor()
                    cursor.execute("SELECT Payable_Amount FROM borrowed_books WHERE Student_ID = %s AND Payment_Status = 'NOT PAID'",(student_id,))
                    amounts = cursor.fetchall()
                    total = sum(amount[0] for amount in amounts)
                    return {"status": "error", "message": f"Clearance denied: Outstanding dues of ₹{total}"}

                else:
                    all_books_returned = Library_clearence.Validation.book_return_status(Id, student_id)
                    if all_books_returned == False:
                        return {"status": "error", "message": "Clearance denied: Books not returned"}

                    else:
                        clearance = Library_clearence.get_library_clearance_certificate(Id, student_id)
                        if clearance == True:
                            return {"status": "success", "message": "Library clearance granted."}
                        else:
                            return {"status": "error", "message": "Clearance failed: An internal issue occurred or clearance not permitted."}

        except Exception as e:
            return {"status": "error", "message": f"Error during clearance check: {str(e)}"}
        

    def update_student(self, newData, originalStudentId):

        # conn = database_connector.connect_to_db(f"{self.get_id()}_library_db")
        # cursor = conn.cursor()
        try:
            connection = database_connector.connect_to_db(f"{self.get_id()}_library_db")
            with connection.cursor() as cursor:
                query = """
                    UPDATE Students
                    SET Student_ID = %s,
                        Student_Name = %s,
                        Date_Of_Birth = %s,
                        Department = %s,
                        Student_Email = %s,
                        Phone_Number = %s,
                        Address = %s,
                        Admission_Year = %s
                    WHERE Student_ID = %s
                """
                data = (
                    newData["Student_ID"].upper(),
                    newData["Student_Name"].upper(),
                    newData["Date_Of_Birth"].upper(),
                    newData["Department"].upper(),
                    newData["Student_Email"].upper(),
                    newData["Phone_Number"].upper(),
                    newData["Address"].upper(),
                    newData["Admission_Year"].upper(),
                    originalStudentId
                )
                cursor.execute(query, data)
            connection.commit()
            if cursor.rowcount:
                return {"success": True}
            else:
                return {"success": False, "message": "Student not found"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def go_back(self):
        """Closes the current webview window."""
        user = self.get_id()
        dashboard_API.open_dashboard(user)
        # webview.windows[0].destroy()

def open_student_dashboard(user_id):
    """
    Opens the Student Dashboard in a webview window.
    """
    # Connect to the specific user's database
    

    # Load HTML template
    html_path = os.path.join(os.path.dirname(__file__), "LMS/templates/student_list.html")
    # html_path = os.path.join(os.path.dirname(__file__), "templates/student_list.html")
    if not os.path.exists(html_path):
        print("Error: student_list.html not found!")
        return

    with open(html_path, "r", encoding="utf-8") as file:
        dashboard_html = file.read()

    api=StudentAPI(user_id)
    webview.windows[0].load_html(dashboard_html)
    webview.windows[0].expose(api.fetchstudents)
    webview.windows[0].expose(api.download)
    webview.windows[0].expose(api.total_student)
    webview.windows[0].expose(api.open_student_entry)
    webview.windows[0].expose(api.clear_student_library)
    webview.windows[0].expose(api.go_back)
    webview.windows[0].expose(api.update_student)
#     webview.create_window(
#                 "Payment Page",
#                 html=dashboard_html,
#                 js_api=api,
#                 width=500,
#                 height=600
#                 # resizable=False
#             )
#     webview.start()
# if __name__ == "__main__":
#     open_student_dashboard("394083")
