import Logics.database_connector as database_connector
import datetime
import Logics.books as assign


class UpdateStock:
    @staticmethod
    def insert_stock(db_name, book_name, author, published_year, edition, publisher, place_of_publication, 
                    qty, price, order_challan_bill_info, source, stock_date, stock_time):
        connection = database_connector.connect_to_db(db_name)
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                    INSERT INTO Book_Stock 
                    (Book_Name, Author, Published_Year, Edition, Publisher, Place_of_Publication, 
                    QTY, Book_Price, Order_Challan_Bill_Info, Source, Stock_Date, Stock_Time, Is_BookID_Assigned) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'NO')
                """
                data = (
                    book_name, author, published_year, edition, publisher, place_of_publication, 
                    qty, price, order_challan_bill_info, source, stock_date, stock_time
                )
                cursor.execute(query, data)
                connection.commit()
                print("Record inserted successfully into Book_Stock table.")


            except Exception as e:
                print("An error occurred while inserting stock information in UPDATE_BOOK_STOCK:", e)
            finally:
                connection.close()

class AddNewStock:
    @staticmethod
    def insert_bookstock(db_name, update_stock):
        connection = None
        try:
            connection = database_connector.connect_to_db(db_name)
            if connection is None:
                print("Failed to connect to the database.")
                return
            # book_name = input_module.get_input("Enter the Book Name: ")
            # author = input_module.get_input("Enter the Author Name: ")
            # published_year = input_module.get_input("Enter Published Year: ")
            # validation.Valid.verify_Year(published_year)
            # edition = input_module.get_input("Enter the Book Edition: ")
            # publisher = input_module.get_input("Enter the Book Publisher: ")
            # place_of_publication = input_module.get_input("Enter the Place Of Publication: ")
            # qty = int(input_module.get_input("Enter the QTY: "))
            # price = float(input_module.get_input("Enter the Price: "))
            # order_challan_bill_info = input_module.get_input("Enter the Order No. / Challan No. & Bill No. / Date: ")
            # source = input_module.get_input("Enter the Source: ")
            stock_date = datetime.date.today()
            stock_time = datetime.datetime.now().time()


            book_name = update_stock["bookName"].upper()
            author = update_stock["author"].upper()
            published_year = update_stock["year"]
            edition = update_stock["edition"].upper()
            publisher = update_stock["publisher"].upper()
            place_of_publication = update_stock["place_of_publication"].upper()
            qty = update_stock["qty"]
            price = update_stock["price"]
            order_challan_bill_info = update_stock["order_challan_bill_info"].upper()
            source = update_stock["source"].upper()
            

            # Insert into Book_Stock table
            UpdateStock.insert_stock(db_name, book_name, author, published_year, edition, publisher, place_of_publication, 
                    qty, price, order_challan_bill_info, source, stock_date, stock_time)

            print("Book and stock information inserted successfully")
            assign.insert_books(db_name, book_name, author)
        except Exception as e:
            print("An error occurred in UPDATE_BOOK_STOCK(insert_bookstock):", e)
        # finally:
        #     if connection:
        #         connection.close()