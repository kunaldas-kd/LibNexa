import os
import webview
import Logics.database_connector as database_connector
import Logics.view_database as view_database
import Logics.handle_menu as handle_menu
import Dashboard_API as dashboard_API

class PassedOutStudentsAPI:
    """API for retrieving passed-out student data from MySQL."""
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return self.user_id

    def fetch_passedout_students(self):
        """
        Fetch and return the passed-out student list from MySQL.
        """
        id = self.get_id()
        try:
            student_list = view_database.view.get_passedout_students(id)
            if not student_list:
                return []
            return [{
                "Sl_No": row[0],
                "Student_ID": row[1],
                "Student_Name": row[2],
                "Certificate_No": row[3],
                "Department": row[4],
                "Student_Email": row[5],
                "Phone_Number": row[6],
                "Passedout_Year": row[7],
                # "Certificate": row[8] if row[8] else ""
            } for row in student_list]
        except Exception as e:
            print(f"Error fetching passed-out students: {e}")
            return []

    def download(self,Department=None,Passedout_Year=None):
        """
        Downloads passed-out student data as a CSV file.
        """
        id = self.get_id()

        res = handle_menu.download_passedout_students(id,Department,Passedout_Year)
        return True if res else False

    def go_back(self):
        """Closes the current webview window and opens the dashboard."""
        user = self.get_id()
        dashboard_API.open_dashboard(user)

def open_passedout_students_dashboard(user_id):
    """
    Opens the Passed-Out Students Dashboard in a webview window.
    """
    
    html_path = os.path.join(os.path.dirname(__file__), "LMS/templates/passedout.html")
    # html_path = os.path.join(os.path.dirname(__file__), "templates/passedout.html")
    if not os.path.exists(html_path):
        print("Error: Passedout.html not found!")
        return

    with open(html_path, "r", encoding="utf-8") as file:
        html = file.read()

    api = PassedOutStudentsAPI(user_id)
    webview.windows[0].load_html(html)
    webview.windows[0].expose(api.fetch_passedout_students)
    webview.windows[0].expose(api.download)
    webview.windows[0].expose(api.go_back)


#     try:
       
    
#         webview.create_window(
#             "Library Clearence",
#             html=dashboard_html,
#             js_api=api,
#             width=500,
#             height=600,
#             # resizable=False
#         )
#     except Exception as e:
#         print(f"Failed to create a WebView2 window: {e}")
#     webview.start()
# if __name__ == "__main__":
#     open_passedout_students_dashboard("306892")  # Replace with actual user_id