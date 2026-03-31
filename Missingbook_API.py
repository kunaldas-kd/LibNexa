import os
import webview
import Logics.missingbook as missingbook  # Handles DB connection
import Dashboard_API as dashboard_API
import Logics.database_connector as database_connector

class MissingBookAPI:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return self.user_id

    def register_missing_book(self, data):

        db_name = f"{self.get_id()}_library_db"
        try:
            
            result = missingbook.missing_book(db_name,data)
            if result == True:
                return {"status": "success", "message": f"Book '{data['bookID']}' registered as {data['reason']}."}
            else:
                return False
        except Exception as e:
            return {"status": "error", "message": f"Database error: {str(e)}"}
    def go_back(self):
        """Closes the current webview window."""
        user = self.get_id()
        dashboard_API.open_dashboard(user)    


def open_missing_book_page(user_id):
    
    html_path = os.path.join(os.path.dirname(__file__), "LMS/templates/Register_Missing_Book.html")
    # html_path = os.path.join(os.path.dirname(__file__), "templates/Register_Missing_Book.html")

    if not os.path.exists(html_path):
        print("Error: HTML template not found.")
        return

    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    api = MissingBookAPI(user_id)
    webview.windows[0].load_html(html_content)
    webview.windows[0].expose(api.register_missing_book)
    webview.windows[0].expose(api.go_back)



#     try:
#         webview.create_window(
#             "Register Missing Book",
#             html=html_content,
#             js_api=api,
#             width=600,
#             height=600
#         )
#         webview.start()
#     except Exception as e:
#         print(f"Failed to create webview window: {e}")

# if __name__ == "__main__":
#     open_missing_book_page("508435")