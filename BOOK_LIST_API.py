import os
import webview
import Logics.database_connector as database_connector
import Logics.view_database as view_database
import Logics.handle_menu as handle_menu
import Dashboard_API as dashboard_API
import Logics.missingbook as book

class BookAPI:
    """API for retrieving book data from MySQL."""
    def __init__(self, Id):
        self.user_id = Id

    def get_id(self):
        return self.user_id
    
    def fetch_books(self):
        """
        Fetch and return the list of books from MySQL.
        """
        id = self.get_id()
        book_list = view_database.view.get_books(id)
        return [{"Book_ID": book[0], "Book_Name": book[1], "Author": book[2],
                 "Published_Year": book[3], "Edition": book[4],
                 "Book_Price": book[5], "Stock_Status": book[6]} for book in book_list]
    
    
    
    def download(self,Book_Name=None, Author=None, Published_Year=None, Stock_Status=None):
        id = self.get_id()
        res = handle_menu.download_books(id,Book_Name, Author, Published_Year, Stock_Status)
        # print (res)
        if res == True:
            # print (res)
            return True
        else:
            return False
    def total_books(self):
        """Closes the login window to return to the main page"""
        id = self.get_id()
        result = book.bookcalculation(id)
        # print(result)
        if result:
            total, instock, outofstock, missingbook = result
            return {
                "total": total,
                "in_stock":instock,
                "out_of_stock": outofstock,
                "missingbook": missingbook
            }
        else:
            return{
                "total": 0,
                "in_stock":0,
                "out_of_stock": 0,
                "missingbook": 0
            }
        
    

    def go_back(self):
        """Closes the current webview window."""
        user = self.get_id()
        dashboard_API.open_dashboard(user)
        # webview.windows[0].destroy()

def open_book_dashboard(Id):
    """
    Opens the Book Dashboard.
    """
    
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "LMS/templates/BOOK_LIST.html")
    # TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates/BOOK_LIST.html")

    if not os.path.exists(TEMPLATE_PATH):
        print("Error: BOOK_LIST.html not found!")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        dashboard_html = file.read()

    api=BookAPI(Id)
    webview.windows[0].load_html(dashboard_html)
    webview.windows[0].expose(api.fetch_books)
    webview.windows[0].expose(api.download)
    webview.windows[0].expose(api.total_books)
    webview.windows[0].expose(api.go_back)
#     webview.create_window(
#             "Payment Page",
#             html=dashboard_html,
#             js_api=api,
#             width=500,
#             height=600
#             # resizable=False
#         )
#     webview.start()
# if __name__ == "__main__":
#     open_book_dashboard("394083")