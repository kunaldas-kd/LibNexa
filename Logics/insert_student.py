import Logics.database_connector as database_connector
import time

def insert_student(connection, student_id, student_name, dob, department, email, phone, address, admission_year):
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO Students 
                (Student_ID, Student_Name, Date_Of_Birth, Department, Student_Email, Phone_Number, Address, Admission_Year) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (student_id, student_name, dob, department, email, phone, address, admission_year)
            cursor.execute(query, data)
        connection.commit()
        print("✅ Student information inserted successfully")
    except Exception as e:
        print(f"❌ Error in insert_student(): {e}")
    finally:
        time.sleep(1)

def student_info(db_name, student_data):
    connection = database_connector.connect_to_db(db_name)
    time.sleep(1)

    if not connection:
        print("❌ Failed to connect to the database.")
        return

    try:
        student_id = student_data.get("student_id", "").strip().upper()
        student_name = student_data.get("student_name", "").strip().upper()
        dob = student_data.get("dob", "").strip()
        department = student_data.get("department", "").strip().upper()
        email = student_data.get("email", "").strip().upper()
        phone = student_data.get("phone", "").strip()
        address = student_data.get("address", "").strip().upper()
        admission_year = student_data.get("admission_year", "").strip().upper()

        insert_student(connection, student_id, student_name, dob, department, email, phone, address, admission_year)
    except Exception as e:
        print(f"❌ Error in student_info(): {e}")
    finally:
        connection.close()
