
import Logics.DOWNLOAD_section as DOWNLOAD_section 
import Logics.Cashbookpdf as Cashbookpdf
from datetime import datetime
def download_books(Id, Book_Name=None, Author=None, Published_Year=None, Stock_Status=None):
    data = DOWNLOAD_section.View.get_books(Id)
    if not Book_Name and not Author and not Published_Year and not Stock_Status:
        return DOWNLOAD_section.excel.download_books_excel(data)
    return DOWNLOAD_section.excel.download_books_excel(data, Book_Name, Author, Published_Year, Stock_Status)

def teacher_borrowed_books(Id,start_date=None, end_date=None):
    data = DOWNLOAD_section.View.get_teacher_borrowed_books(Id)
    if not start_date and not end_date:
        return DOWNLOAD_section.excel.download_teacher_borrowed_books_excel(data)
    return DOWNLOAD_section.excel.download_teacher_borrowed_books_excel(data,start_date, end_date)
    
def download_teachers(Id,Department=None, Designation=None, Joining_Year=None, Employment_Status=None):
    data = DOWNLOAD_section.View.get_teachers(Id)
    if Department and not Designation and not Joining_Year and not Employment_Status:    
        return DOWNLOAD_section.excel.download_teachers_excel(data)
    return DOWNLOAD_section.excel.download_teachers_excel(data, Department, Designation, Joining_Year, Employment_Status)

def download_students(Id, dept = None, admission = None):
    data = DOWNLOAD_section.View.get_students(Id)
    if not dept and not admission:
        return DOWNLOAD_section.excel.download_students_excel(data)
    return DOWNLOAD_section.excel.download_students_excel(data, dept, admission)

    
def download_book_stock(Id, Book_Name=None,Author=None,
                        Publisher=None,Place_of_Publication=None,Source=None,
                        Stock_Date=None,Published_Year=None,Order_Challan_Bill_Info=None):
    data = DOWNLOAD_section.View.get_book_stock(Id)
    print(data)
    if not Book_Name and not Author and not Publisher and not Place_of_Publication and not Source and not Stock_Date and not Published_Year and not Order_Challan_Bill_Info:
        return DOWNLOAD_section.excel.download_stocks_excel(data)
    
    return DOWNLOAD_section.excel.download_stocks_excel(data,Book_Name,Author,
                                                            Publisher,Place_of_Publication,
                                                            Source,Stock_Date,Published_Year,
                                                            Order_Challan_Bill_Info)
    

def download_borrowed_books(Id, start_date=None, stop_date=None):
    data = DOWNLOAD_section.View.get_borrowed_books(Id)
    if not start_date and not stop_date:
        return DOWNLOAD_section.excel.download_borrowed_books_excel1(data)
    return DOWNLOAD_section.excel.download_borrowed_books_excel(data, start_date, stop_date)

    
def download_passedout_students(Id,Department=None,Passedout_Year=None):
    data = DOWNLOAD_section.View.get_passedout_students(Id)
    if not Department and not Passedout_Year:
        DOWNLOAD_section.excel.download_passedout_students_excel(data,Department,Passedout_Year)
    return DOWNLOAD_section.excel.download_passedout_students_excel(data,Department,Passedout_Year) 
    

def download_cash_book(Id,Department=None,Passedout_Year=None):
    month = datetime.now().strftime("%B")
    data = DOWNLOAD_section.View.get_cash_transactions(Id)
    if not Department and not Passedout_Year:
        filename=f"Cash_Transactions_Report-{month}.pdf"
        return Cashbookpdf.generate_cash_transactions_pdf(data,None,None, filename)
    return Cashbookpdf.generate_cash_transactions_pdf(data, Department, Passedout_Year, None) 
    
    
