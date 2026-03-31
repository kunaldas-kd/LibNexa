import random
import string
import datetime
import Logics.database_connector as database_connector

def generate_password():
    """Generates a random password with 3 numbers and 5 letters."""
    letters = ''.join(random.choices(string.ascii_letters, k=5))
    numbers = ''.join(random.choices(string.digits, k=3))
    password = letters + numbers
    password_list = list(password)
    random.shuffle(password_list)
    return ''.join(password_list)




def get_overdue_books(Id):
    user_db_name = f"{Id}_library_db"
    connection = database_connector.connect_to_db(user_db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT Student_ID, Student_Name, Book_Name, Return_Date FROM borrowed_books WHERE Submit = 0")
    info = cursor.fetchall()

    overdue_books = []

    for row in info:
        Student_ID, Student_Name, Book_Name, return_date = row

        # Convert return_date to datetime.date if needed
        if isinstance(return_date, str):
            return_date_obj = datetime.datetime.strptime(return_date, "%Y-%m-%d").date()
        elif isinstance(return_date, datetime.datetime):
            return_date_obj = return_date.date()
        else:
            return_date_obj = return_date  # already a datetime.date

        # Check if the book is overdue
        if return_date_obj < datetime.date.today():
            overdue_books.append({
                "Student_ID": Student_ID,
                "Student_Name": Student_Name,
                "Book_Name": Book_Name,
                "Due_Date": return_date_obj.strftime("%d-%m-%Y")
            })

    connection.close()  # ✅ always close the connection
    return overdue_books