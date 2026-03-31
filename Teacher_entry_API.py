import os
import Logics.file_finding as file_finding
import webview
from Logics.teacher_entry import teacher_info  # You need this module as you created earlier
from Logics.UPLOAD_DATA import TEACHERS         # Assumes you have a class for processing Excel files for teachers
import Logics.database_connector as database_connector
import Logics.validation as validation
import Teacher_List_API as dashboard_API        # A teacher dashboard module similar to student one

class TeacherEntryAPI:
    def __init__(self, Id):
        self.data = Id

    def get_id(self):
        return self.data

    def submit_Teacher_Info(self, teacher_data):
        """
        Submits individual teacher information to the database.
        Expects teacher_data to be a dictionary with details.
        """
        Id = self.get_id()
        if not Id or not teacher_data:
            return "Error: Missing 'Id' or 'teacher_data' parameters!"

        user_db_name = f"{Id}_library_db"
        print("Using database:", user_db_name)

        try:
            # Basic validation
            res = validation.Valid.verify_phone_number(teacher_data.get("phone", "").strip())
            res1 = validation.Valid.verify_admission_year(teacher_data.get("joining_year", "").strip())
            res2 = validation.Valid.verify_email(teacher_data.get("email", "").strip())
            print(res)
            print(res1)
            print(res2)
            if not res:
                return {"phone": False}
            elif not res1:
                return {"joining_year": False}
            elif not res2:
                return {"email": False}
            else:
                result = teacher_info(user_db_name, teacher_data)
                print(result)
                if result == True:
                    return True
                else:
                    return False
        except Exception as e:
            return f"Error during teacher information submission: {str(e)}"

    def uploadTeacherData(self, file_name):
        Id = self.get_id()
        user_db_name = f"{Id}_library_db"
        found_path = file_finding.search(file_name)
        TEACHERS.process_files(found_path, user_db_name)
        return f"Excel file '{file_name}' processed successfully!"

    def go_back(self):
        user = self.get_id()
        dashboard_API.open_teacher_dashboard(user)


def open_teacher_entry(Id):
    
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/teacher_entry.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/teacher_entry.html")

    if not os.path.exists(TEMPLATE_PATH):
        print("Error: teacher_entry.html not found!")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        teacher_entry_html = file.read()

    api = TeacherEntryAPI(Id)
    webview.windows[0].load_html(teacher_entry_html)
    webview.windows[0].expose(api.submit_Teacher_Info)
    webview.windows[0].expose(api.uploadTeacherData)
    webview.windows[0].expose(api.go_back)

#     try:
#         # Create a window for the student entry interface.
#         window = webview.create_window(
#             "Student Entry",
#             html=teacher_entry_html,
#             js_api=api,width= 1000,
#             height= 600,
#             fullscreen=False
#         )
#     except Exception as e:
#         print(f"Failed to create a WebView2 window: {e}")
#     # window.maximize()
    
#     webview.start()

# # Uncomment these lines to test the interface locally:
# if __name__ == "__main__":
#     open_teacher_entry('877509')

