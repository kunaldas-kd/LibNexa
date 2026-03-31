import os
import webview
import Logics.database_connector as database_connector  # Module for establishing the database connection.
import Logics.validation as validation
import Logics.file_finding as file_finding
from Logics.UPLOAD_DATA import STOCK
from Logics.UPDATE_BOOK_STOCK import AddNewStock
import BOOK_STOCK_API as dashboard_API

class UpdateStockAPI:
    def __init__(self, Id):
        self.data = Id  # Store the user ID for reuse

    def get_id(self):
        return self.data
    
    def submit_Book_Info(self, update_stock):
        """
        Submits individual student information to the database.
        Expects student_data to be a dictionary with details.
        """
        Id = self.get_id()
        if not Id or not update_stock:
            return "Error: Missing 'Id' or 'student_data' parameters!"

        # Construct a user-specific database name.
        user_db_name = f"{Id}_library_db"
        print("Using database:", user_db_name)
        try:
            # Insert the student data into the database.

            res = validation.Valid.verify_Year(update_stock.get("year", "").strip())
            if res == False:
                return {"year" : False}
            else:
                result = AddNewStock.insert_bookstock(user_db_name, update_stock)
                # If the function returns None, assume success.
                if result is None:
                    return "Books information inserted successfully!"
                else:
                    return result
        except Exception as e:
            return f"Error during Books information submission: {str(e)}"

    def upload_Book_Data(self, file_name):
        try:
            Id = self.get_id()
            user_db_name = f"{Id}_library_db"
            found_path = file_finding.search(file_name)
            # Process the Excel file using the found path.
            STOCK.process_files(found_path, user_db_name)
            return f"Excel file '{file_name}' processed successfully!"
        except Exception as e:
            return f"Error processing Excel file: {str(e)}"



    def go_back(self):
        """Closes the current webview window."""
        user = self.get_id()
        dashboard_API.open_Book_Stocks(user)
        # webview.windows[0].destroy()

def open_update_stock(Id):
    """
    Opens the Update Stock Page using pywebview.
    Loads the HTML template and calls the above API methods.
    """
    # Define the database name based on the ID
    
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/update_stock.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/update_stock.html")
    if not os.path.exists(TEMPLATE_PATH):
        print("Error: update_stock.html not found!")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        update_stock_html = file.read()
    webview.windows[0].load_html(update_stock_html)
    api = UpdateStockAPI(Id)  # Adjust API call to use the ID parameter
    webview.windows[0].expose(api.go_back)
    webview.windows[0].expose(api.upload_Book_Data)
    webview.windows[0].expose(api.submit_Book_Info)
#     try:
#         # Create a window for the update stock interface.
#         window = webview.create_window(
#             "Update Stock",
#             html=update_stock_html,
#             js_api=api,width= 1000,
#             height= 600,
#             fullscreen=False
#         )
#     except Exception as e:
#         print(f"Failed to create a WebView2 window: {e}")
#     webview.start()
#     # window.maximize()
# # Uncomment these lines to test the interface locally:
# if __name__ == "__main__":
#     open_update_stock('394083')