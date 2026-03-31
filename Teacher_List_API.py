import os
import webview
import Logics.database_connector as database_connector
import Logics.view_database as view_database
import Logics.handle_menu as handle_menu
import Dashboard_API as dashboard_API
import Logics.missingbook as total_teacher  # Can be renamed
import Logics.database_connector as database_connector
from Logics.Borrow_Register import valid_payment
import Logics.Library_clearence as Library_clearence # You must create this file with open_teacher_entry()
import Teacher_entry_API
import Logics.CHECK_INTERNET as CHECK_INTERNET

class TeacherAPI:
    """API for retrieving teacher data from MySQL."""
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return self.user_id

    def fetch_teachers(self):
        """
        Fetch and return the list of teachers from MySQL.
        """
        id = self.get_id()
        try:
            teacher_list = view_database.view.get_teachers(id)
            # print(teacher_list)
            if not teacher_list:
                return []
            return list({
                "Teacher_ID": teacher["Teacher_ID"],
                "Teacher_Name": teacher["Teacher_Name"],
                "Designation": teacher["Designation"],
                "Department": teacher["Department"],
                "Teacher_Email": teacher["Teacher_Email"],
                "Phone_Number": teacher["Phone_Number"],
                "Address": teacher["Address"],
                "Joining_Year": teacher["Joining_Year"],
                "Employment_Status": teacher["Employment_Status"]
            } for teacher in teacher_list)
        except Exception as e:
            print(f"\u274c Error fetching teachers: {e}")
            return []

    def download(self, Department=None, Designation=None, Joining_Year=None, Employment_Status=None):
        id = self.get_id()
        res = handle_menu.download_teachers(id, Department, Designation, Joining_Year, Employment_Status)
        if res == True:
            # print (res)
            return True
        else:
            return False

    def total_teacher(self):
        id = self.get_id()
        return total_teacher.Total_teacher(id)

    def open_teacher_entry(self):
        id = self.get_id()
        Teacher_entry_API.open_teacher_entry(id)

    def open_teacher_exit(self,teacher_id):
        # id = self.get_id()
        # Library_clearance_API_for_teachers.open_teacher_clearance_page(id)
        Id = self.get_id()
        if not Id or not teacher_id:
            return {"status": "error", "message": "Missing user ID or teacher ID"}

        user_db_name = f"{Id}_library_db"

        try:
            result = CHECK_INTERNET.is_connected()
            if result == False:
                return {"check_internet": False}
            else:
                all_books_returned = Library_clearence.Validation.book_return_status_for_teacher(Id, teacher_id)
                if all_books_returned is False:
                    return {"status": "error", "message": "Clearance denied: Books not returned"}

                else:
                    clearance = Library_clearence.get_teacher_clearance_certificate1(Id, teacher_id)
                    if clearance is True:
                        return {"status": "success", "message": "Library clearance granted."}
                    else:
                        return {"status": "error", "message": "Clearance failed: An internal issue occurred or clearance not permitted."}

        except Exception as e:
            return {"status": "error", "message": f"Error during clearance check: {str(e)}"}
        
    def update_teacher(self, newData, originalTeacherId):
        try:
            connection = database_connector.connect_to_db(f"{self.get_id()}_library_db")
            with connection.cursor() as cursor:
                query = """
                    UPDATE Teachers
                    SET Teacher_ID = %s,
                        Teacher_Name = %s,
                        Designation = %s,
                        Department = %s,
                        Teacher_Email = %s,
                        Phone_Number = %s,
                        Address = %s,
                        Joining_Year = %s
                    WHERE Teacher_ID = %s
                """
                data = (
                    newData["Teacher_ID"].upper(),
                    newData["Teacher_Name"].upper(),
                    newData["Designation"].upper(),
                    newData["Department"].upper(),
                    newData["Teacher_Email"].upper(),  # Keep original case for emails
                    newData["Phone_Number"],   # Don't uppercase numbers
                    newData["Address"].upper(),
                    newData["Joining_Year"],   # Don't uppercase years
                    originalTeacherId
                )
                cursor.execute(query, data)
                rows_affected = cursor.rowcount
            
            connection.commit()
            
            if rows_affected > 0:
                return {"success": True}
            else:
                return {"success": False, "message": "Teacher not found"}
                
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    def go_back(self):
        user = self.get_id()
        dashboard_API.open_dashboard(user)


def open_teacher_dashboard(user_id):
    """
    Opens the Teacher Dashboard in a webview window.
    """
    html_path = os.path.join(os.path.dirname(__file__), "LMS/templates/teacher_list.html")
    # html_path = os.path.join(os.path.dirname(__file__), "templates/teacher_list.html")
    if not os.path.exists(html_path):
        print("\u274c Error: teacher_list.html not found!")
        return

    with open(html_path, "r", encoding="utf-8") as file:
        dashboard_html = file.read()

    api = TeacherAPI(user_id)
    webview.windows[0].load_html(dashboard_html)
    webview.windows[0].expose(api.fetch_teachers)
    webview.windows[0].expose(api.download)
    webview.windows[0].expose(api.total_teacher)
    webview.windows[0].expose(api.open_teacher_entry)
    webview.windows[0].expose(api.open_teacher_exit)
    webview.windows[0].expose(api.go_back)
    webview.windows[0].expose(api.update_teacher)
#     try:
#         # Create a window for the student entry interface.
#         window = webview.create_window(
#             "Student Entry",
#             html=dashboard_html,
#             js_api=api,width= 1000,
#             height= 600,
#             fullscreen=False
#         )
#     except Exception as e:
#         print(f"Failed to create a WebView2 window: {e}")
#     # window.maximize()

#     webview.start()

# # # Uncomment these lines to test the interface locally:
# if __name__ == "__main__":
#     open_teacher_dashboard('394083')
