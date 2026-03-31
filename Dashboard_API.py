import os
import webview
import Logics.database_connector as database_connector
import Main as main
import Missingbook_API as missingbook_API
import base64
import Teacher_List_API
import Teacher_Register_API
import Book_issue_register_API as Book_issue_register_API
# import Payment_API as payment_API
import Student_list_API as Student_list_API
import BOOK_LIST_API as BOOK_LIST_API
import BOOK_STOCK_API as BOOK_STOCK_API
import View_Borrow_Register_API as view_Borrow_Register_API
import Logics.password_generator as fund
import PASSEDOUT_API as PASSEDOUT_API
import Cashbook_API as Cashbook_API
import Book_Recovery_API as BRA
import Setting_API
import Logics.missingbook as Total

class dashboardAPI:
    """Class to handle interactions between the HTML templates and backend logic."""

    def __init__(self, Id):
        self.data = Id  # Store the user ID for reuse

    def get_id(self):
        return self.data

    def open_teacher_list(self):
        """Opens the Student Entry page."""
        id = self.get_id()
        Teacher_List_API.open_teacher_dashboard(id)
        

    def teacher_register(self):
        """Opens the Manage Books page."""
        id = self.get_id()
        Teacher_Register_API.open_teacher_borrow_dashboard(id)
        
    def passedout_students_view(self):
        id = self.get_id()
        PASSEDOUT_API.open_passedout_students_dashboard(id)

    def student_view(self):
        id = self.get_id()
        Student_list_API.open_student_dashboard(id)
        

    def book_view(self):
        id = self.get_id()
        BOOK_LIST_API.open_book_dashboard(id)
      
    def cash_book(self):
        id=self.get_id()
        Cashbook_API.open_cashbook_dashboard(id)

    def book_stock_view(self):
        id = self.get_id()
        BOOK_STOCK_API.open_Book_Stocks(id)

    def borrow_register_view(self):
        id = self.get_id()
        view_Borrow_Register_API.open_borrow_register_dashboard(id)
        

    def MissingBook(self):
        id = self.get_id()
        missingbook_API.open_missing_book_page(id)

    def BOOKRECOVERY(self):
        id = self.get_id()
        BRA.open_recovery_page(id)

    def settings(self):
        id = self.get_id()
        Setting_API.open_settings(id)

    def reminderboard(self):
        id = self.get_id()
        return fund.get_overdue_books(id)
    def total_issued(self):
        """Calculate total books issued to both students and teachers."""
        try:
            user_id = self.get_id()
            
            # Get student issued books
            student_result = Total.Total_Issued(user_id)
            print(f"Student result type: {type(student_result)}, value: {student_result}")
            
            student_total = 0
            if student_result and isinstance(student_result, tuple) and len(student_result) > 0:
                first_element = student_result[0]
                # Handle nested list structure like [(0,)]
                if isinstance(first_element, list) and len(first_element) > 0:
                    if isinstance(first_element[0], tuple) and len(first_element[0]) > 0:
                        student_total = first_element[0][0]  # Extract from [(0,)]
                    elif isinstance(first_element[0], (int, float)):
                        student_total = first_element[0]
                elif isinstance(first_element, (int, float)):
                    student_total = first_element
            
            # Get teacher issued books
            teacher_result = Total.Total_Teacher_Issued(user_id)
            print(f"Teacher result type: {type(teacher_result)}, value: {teacher_result}")
            
            teacher_total = 0
            if teacher_result and isinstance(teacher_result, tuple) and len(teacher_result) > 0:
                # Teacher result appears to be (0, 0, 0) - first element is the total
                if isinstance(teacher_result[0], (int, float)):
                    teacher_total = teacher_result[0]
            
            # Ensure both values are numeric
            student_total = int(student_total) if isinstance(student_total, (int, float)) else 0
            teacher_total = int(teacher_total) if isinstance(teacher_total, (int, float)) else 0
            
            total = student_total + teacher_total
            
            # Debug print (consider using logging instead)
            print(f"Student issued: {student_total}, Teacher issued: {teacher_total}, Total: {total}")
            
            return {"total": total}
            
        except Exception as e:
            print(f"Error calculating total issued: {e}")
            return {"total": 0}

    def total_teacher(self):
        """Get total number of teachers."""
        try:
            user_id = self.get_id()
            result = Total.Total_teacher(user_id)
            return {"total": result} if result is not None else {"total": 0}
        except Exception as e:
            print(f"Error getting teacher count: {e}")
            return {"total": 0}

    def total_student(self):
        """Get total number of students."""
        try:
            user_id = self.get_id()
            result = Total.Total_student(user_id)
            return {"total": result} if result is not None else {"total": 0}
        except Exception as e:
            print(f"Error getting student count: {e}")
            return {"total": 0}

    def total_books(self):
        """Get total number of books in the library."""
        try:
            user_id = self.get_id()
            result = Total.bookcalculation(user_id)
            
            if result:
                total, in_stock, out_of_stock, missing_books = result
                return {
                    "total": total,
                    "in_stock": in_stock,
                    "out_of_stock": out_of_stock,
                    "missing_books": missing_books
                }
            else:
                return {
                    "total": 0,
                    "in_stock": 0,
                    "out_of_stock": 0,
                    "missing_books": 0
                }
                
        except Exception as e:
            print(f"Error calculating book totals: {e}")
            return {
                "total": 0,
                "in_stock": 0,
                "out_of_stock": 0,
                "missing_books": 0
            }

    def institutename(self):
        user_id = self.get_id()
        connection = database_connector.connect_to_db(f"{user_id}_library_db")
        cursor = connection.cursor()
        cursor.execute('''SELECT Institute_name FROM users''')
        results = cursor.fetchone()
        return results

def open_dashboard(Id):
    """
    Opens the main dashboard page if the database connection is successful.
    """

    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/dashboard.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/dashboard.html")

    if not os.path.exists(TEMPLATE_PATH):
        print("Error: dashboard.html not found!")
        return

    logo_path = os.path.join(os.path.dirname(__file__), "LMS/templates/logo1.png")
    # logo_path = os.path.join(os.path.dirname(__file__), "templates/logo1.png")
    with open(logo_path, "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    logo_data_url = f"data:image/png;base64,{logo_base64}"
    
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        dashboard_html = file.read()

    dashboard_html = dashboard_html.replace("{{logo_path}}", logo_data_url)

    
    api = dashboardAPI(Id)
    webview.windows[0].load_html(dashboard_html)
    webview.windows[0].expose(api.open_teacher_list)
    webview.windows[0].expose(api.book_stock_view)
    webview.windows[0].expose(api.book_view)
    webview.windows[0].expose(api.borrow_register_view)
    webview.windows[0].expose(api.student_view)
    webview.windows[0].expose(api.MissingBook)
    webview.windows[0].expose(api.passedout_students_view)
    webview.windows[0].expose(api.cash_book)
    webview.windows[0].expose(api.BOOKRECOVERY)
    webview.windows[0].expose(api.settings)
    webview.windows[0].expose(api.teacher_register)
    webview.windows[0].expose(api.reminderboard)
    webview.windows[0].expose(api.total_books)
    webview.windows[0].expose(api.total_issued)
    webview.windows[0].expose(api.total_student)
    webview.windows[0].expose(api.total_teacher)
    webview.windows[0].expose(api.institutename)


# #         # Create the dashboard window
#     try:
#         window = webview.create_window("Dashboard", html=dashboard_html, js_api=api,width= 1000,
#     height= 600, fullscreen=False)
#         webview.start()
#     except Exception as e:
#         print(f"Failed to create a WebView2 window: {e}")

#     # else:
#         # print(f"Error: Unable to connect to the database '{user_db_name}'.")
#     # window.maximize()


# if __name__ == "__main__":
#     open_dashboard("394083")
    

        
