import os
import Logics.file_finding as file_finding
import webview
from Logics.insert_student import student_info    # Module for inserting a student row into the database.
from Logics.UPLOAD_DATA import STUDENTS             # Module/class to handle Excel file processing.
import Logics.database_connector as database_connector  # Module for establishing the database connection.
import Logics.validation as validation
import Student_list_API as dashboard_API

class StudentEntryAPI:
    def __init__(self, Id):
        self.data = Id  # Store the user ID for reuse

    def get_id(self):
        return self.data

    
    def submit_Student_Info(self, student_data):
        """
        Submits individual student information to the database.
        Expects student_data to be a dictionary with details.
        """
        Id = self.get_id()
        if not Id or not student_data:
            return "Error: Missing 'Id' or 'student_data' parameters!"

        # Construct a user-specific database name.
        user_db_name = f"{Id}_library_db"
        print("Using database:", user_db_name)
        try:
            # Insert the student data into the database.

            res = validation.Valid.verify_phone_number(student_data.get("phone", "").strip())
            # res1 = validation.Valid.valid_semester(student_data.get("semester", "").strip())
            # res2 = validation.Valid.valid_standard(student_data.get("standard", "").strip())
            res3 = validation.Valid.verify_admission_year(student_data.get("admission_year", "").strip())
            res4 = validation.Valid.verify_email(student_data.get("email", "").strip())
            if res == False:
                return {"phone" : False}
            elif res3 == False:
                return {"admission_year" : False}
            elif res4 == False:
                return {"email" : False}
            else:
                result = student_info(user_db_name, student_data)
                # If the function returns None, assume success.
                if result is None:
                    return "Student information inserted successfully!"
                else:
                    return result
        except Exception as e:
            return f"Error during student information submission: {str(e)}"

    def uploadStudentData(self, file_name):
        # try:
        Id = self.get_id()
        user_db_name = f"{Id}_library_db"
        found_path = file_finding.search(file_name) 
        # Process the Excel file using the found path.
        STUDENTS.process_files(found_path, user_db_name)
        return f"Excel file '{file_name}' processed successfully!"
        # except Exception as e:
        #     print("Error processing Excel file: {str(e)}")
        #     return f"Error processing Excel file: {str(e)}"

    def go_back(self):
        """Closes the current webview window."""
        user = self.get_id()
        dashboard_API.open_student_dashboard(user)
        # webview.windows[0].destroy()

    # def go_back(self):
    #     """Closes the current webview window."""
    #     user = self.get_id()
    #     student_view_page.open_student_view(user)
    #     webview.windows[0].destroy()


def open_student_entry(Id):
    """
    Opens the student entry interface using pywebview.
    Loads the HTML template and calls the above API methods.
    """
    
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/student_entry.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/student_entry.html")
    if not os.path.exists(TEMPLATE_PATH):
        print("Error: student_entry.html not found!")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        student_entry_html = file.read()

    api = StudentEntryAPI(Id)
    webview.windows[0].load_html(student_entry_html)
    webview.windows[0].expose(api.submit_Student_Info)
    webview.windows[0].expose(api.uploadStudentData)
    webview.windows[0].expose(api.go_back)
    
#     try:
#         # Create a window for the student entry interface.
#         window = webview.create_window(
#             "Student Entry",
#             html=student_entry_html,
#             js_api=api,width= 1000,
#     height= 600,
#             fullscreen=False
#         )
#     except Exception as e:
#         print(f"Failed to create a WebView2 window: {e}")
#     # window.maximize()

#     webview.start()

# # Uncomment these lines to test the interface locally:
# if __name__ == "__main__":
#     open_student_entry('394083')
