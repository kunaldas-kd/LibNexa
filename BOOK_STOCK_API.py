import os
import webview
import Logics.database_connector as database_connector
import Logics.view_database as view_database
from datetime import timedelta , datetime
import Logics.handle_menu as handle_menu
import Dashboard_API as dashboard_API
import Logics.missingbook as Totalbooks
import Update_stock
from Logics.books import insert_books 

def format_timedelta(td):
    if isinstance(td, timedelta):
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return ""
class Book_Stock_API:
    """API for retrieving book stock data from MySQL."""
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return self.user_id

    def fetchbookstock(self):
        """
        Fetch and return the list of books from MySQL.
        """
        id = self.get_id()
        try:
            book_list = view_database.view.get_book_stock(id)  # Updated this line
            if not book_list:
                return []
            return [{
                "SL_No": book[0],
                "Book_Name": book[1],
                "Author": book[2],
                "Edition": book[3],
                "Publisher": book[4],
                "Place_of_Publication": book[5],
                "Published_Year": book[6],
                "QTY": book[7],
                "Book_Price": book[8],
                "Order_Challan_Bill_Info": book[9],
                "Source": book[10],
                "Stock_Date": book[11].isoformat() ,
                "Stock_Time": format_timedelta(book[12]),
                "Is_BookID_Assigned": book[13]
            } for book in book_list]
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []
        
    def download(self,Book_Name=None,Author=None,
                        Publisher=None,Place_of_Publication=None,Source=None,
                        Stock_Date=None,Published_Year=None,Order_Challan_Bill_Info=None):
        id = self.get_id()
        # parsed_date = datetime.strptime(Stock_Date, "%Y-%m-%d")
        res = handle_menu.download_book_stock(id,Book_Name,Author,
                        Publisher,Place_of_Publication,Source,
                        Stock_Date,Published_Year,Order_Challan_Bill_Info)
        # print (res)
        if res == True:
            # print (res)
            return True
        else:
            return False
    def total_books(self):
        """Closes the login window to return to the main page"""
        id = self.get_id()
        result = Totalbooks.bookcalculation(id)
        # print(result[0])
        if result:
            return result[0]
        else:
            return result[0]
        
    def add_book_stock(self):
        """Opens the Update Stock page."""
        id = self.get_id()
        Update_stock.open_update_stock(id)

    def Id_Assign(self, addbooks):
        """
        Inserts book details into user-specific database.
        Expected format for 'addbooks':
        {
            "id": "101",
            "bookName": "Python Basics",
            "author": "John Doe"
        }
        """
        # print(addbooks)
        Id = self.get_id()
        if not Id or not addbooks:
            return "Error: Missing 'Id' or 'addbooks'!"

        user_db_name = f"{Id}_library_db"
        print("Using database:", user_db_name)

        try:
            result = insert_books(user_db_name, addbooks)
            return True if result is True else False
        except Exception as e:
            return f"Error during Books ID assign: {str(e)}"

    def go_back(self):
        """Closes the current webview window."""
        user = self.get_id()
        dashboard_API.open_dashboard(user)
        # webview.windows[0].destroy()

def open_Book_Stocks(user_id):
    """
    Opens the Book Stock Dashboard in a webview window.
    """
    html_path = os.path.join(os.path.dirname(__file__), "LMS/templates/Book_Stocks.html")
    # html_path = os.path.join(os.path.dirname(__file__), "templates/Book_Stocks.html")
    if not os.path.exists(html_path):
        print("Error: Book_Stocks.html not found!")
        return

    with open(html_path, "r", encoding="utf-8") as file:
        dashboard_html = file.read()

    api = Book_Stock_API(user_id)

    api=Book_Stock_API(user_id)
    webview.windows[0].load_html(dashboard_html)
    webview.windows[0].expose(api.fetchbookstock)
    webview.windows[0].expose(api.download)
    webview.windows[0].expose(api.total_books)
    webview.windows[0].expose(api.add_book_stock)
    webview.windows[0].expose(api.go_back)
    webview.windows[0].expose(api.Id_Assign)

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
#     open_Book_Stocks("394083")
