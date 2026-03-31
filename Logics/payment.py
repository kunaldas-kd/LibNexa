import Logics.database_connector as database_connector
import Logics.Get_balance as credit
import random
from datetime import datetime
# import database_connector as database_connector
# import Logics.Get_balance as credit
def payment(Id, student):
    connection = None
    cursor = None
    try:
        connection = database_connector.connect_to_db(Id)

        if not connection:
            return False
        else:
            cursor = connection.cursor()
            query = '''SELECT Submit FROM borrowed_books WHERE Student_ID = %s'''
            cursor.execute(query, (student,))
            results = cursor.fetchall()
            print(results)
            # if any(value == 0 for value in results):
            #     return False
            # Only proceed if student_id processing is fully complete
            if all(value[0] == 1 for value in results):
            
                query1 = """SELECT Payable_Amount FROM borrowed_books WHERE Student_ID = %s AND Payment_Status = %s """
                cursor.execute(query1, (student, 'NOT PAID'))
                results1 = cursor.fetchall()
                print(results1)
                if results1 is None:
                    print("No unpaid records found for the student.")
                    return False
                for result1 in results1:
                    Amount = result1[0]
                    print(Amount)
                    combination = ''.join(str(random.randint(0, 9)) for _ in range(9))
                    Transaction_ID = f"T{combination}"
                    Transaction_Date = datetime.now().date()
                    student_id = student.upper()
                    previousbalance = credit.credit(Id)
                    
                    presentbalance = previousbalance + Amount

                    print(f"PRESENT BALANCE {presentbalance}")
                    insert_query = '''
                        INSERT INTO cash_book (
                            Transaction_ID, Student_ID, Transaction_Date, Description,
                            Transaction_Type, Amount, Credit, Debit, Balance
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                    cursor.execute(insert_query, (
                        Transaction_ID.upper(), student_id.upper(), Transaction_Date, "FOR LATE SUBMISSION", "CASH",
                        Amount, True, False, presentbalance
                    ))

                    query3 = '''UPDATE borrowed_books
                                SET Payment_Status = %s, Payable_Amount = %s
                                WHERE Student_ID = %s AND Payment_Status = 'NOT PAID' '''
                    cursor.execute(query3, ('PAID', 0.00, student))
                    connection.commit()

                    print("Payment Success.")
                    print(f"Student ID: {student} has been unblocked.")
                    
                return True
            else:
                return False
            
    except Exception as e:
        print("An error occurred in Payment:", e)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        
# payment("730540_library_db", "SID1000")