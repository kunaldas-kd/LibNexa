from datetime import datetime
import Logics.database_connector as database_connector
# import database_connector
def passedout_student(id, student_id, certificate_no, pdf_data):
    connection = None
    cursor = None
    # try:
    # Connect to the database
    connection = database_connector.connect_to_db(id)
    if not connection:
        print("Database connection failed.")
        return False
    cursor = connection.cursor()
    try:
        # Get book details
        student_query = '''
        SELECT Student_ID, Student_Name, Department, Student_Email, Phone_Number
        FROM students
        WHERE Student_ID = %s
        '''
        cursor.execute(student_query, (student_id,))
        student = cursor.fetchone()

        Student_ID = student[0]
        Student_Name = student[1]
        Department = student[2]
        Student_Email = student[3]
        Phone_Number = student[4]

        Passedout_Year = datetime.now().year

        print(Student_ID)
        print(Student_Name)
        print(Department)
        print(Student_Email)
        print(Phone_Number)
        print(Passedout_Year)
        insert_query = '''
            INSERT INTO Passedout_Students (
                Student_ID, Student_Name, Certificate_No, Department,
                Student_Email, Phone_Number, Passedout_Year, Certificate
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''

        cursor.execute(insert_query, (
            Student_ID, Student_Name, certificate_no, Department,
            Student_Email, Phone_Number, Passedout_Year, pdf_data
        ))

        #   4. Delete from the original 'students' table
        delete_sql = "DELETE FROM students WHERE Student_ID = %s"
        cursor.execute(delete_sql, (student_id,))

        # 5. Commit the transaction
        connection.commit()
        print(f"✅ Student '{student_id}' moved to PassedOut_Students (Year: {Passedout_Year}).")
        return True

    except Exception as e:
        # Roll back any partial changes on error
        if connection:
            connection.rollback()
        print(f"❌ Error while passing out student: {e}")
        return False

    finally:
        # Always close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# passout_student("671358_library_db" , "D212206708","0123456789")