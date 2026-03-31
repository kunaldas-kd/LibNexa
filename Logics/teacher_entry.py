import Logics.database_connector as database_connector
import time

def insert_teacher(connection, teacher_id, teacher_name, designation, department, email, phone, address, joining_year, employment_status):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Teacher_ID FROM teachers")
            TID = cursor.fetchall()
            if any(value[0] == teacher_id for value in TID):
                cursor.execute('''UPDATE teachers SET Teacher_Name = %s, Designation = %s, Department = %s, Teacher_Email = %s, Phone_Number = %s, Address = %s, Joining_Year = %s, Employment_Status = %s WHERE Teacher_ID = %s''',
                               (teacher_name, designation, department, email,phone, address, joining_year, employment_status, teacher_id))
                connection.commit()
                return True
            query = """
                INSERT INTO Teachers 
                (Teacher_ID, Teacher_Name, Designation, Department, Teacher_Email, Phone_Number, Address, Joining_Year, Employment_Status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                teacher_id, teacher_name, designation,
                department, email, phone,
                address, joining_year, employment_status
            )
            cursor.execute(query, data)
        connection.commit()
        print("✅ Teacher information inserted successfully")
        return True
    except Exception as e:
        print(f"❌ Error in insert_teacher(): {e}")
    finally:
        time.sleep(1)

def teacher_info(db_name, teacher_data):
    connection = database_connector.connect_to_db(db_name)
    time.sleep(1)

    if not connection:
        print("❌ Failed to connect to the database.")
        return

    try:
        teacher_id = teacher_data.get("teacher_id", "").strip().upper()
        teacher_name = teacher_data.get("teacher_name", "").strip().upper()
        designation = teacher_data.get("designation", "").strip().upper()
        department = teacher_data.get("department", "").strip().upper()
        email = teacher_data.get("email", "").strip().upper()
        phone = teacher_data.get("phone", "").strip()
        address = teacher_data.get("address", "").strip().upper()
        joining_year = teacher_data.get("joining_year", "").strip().upper()
        employment_status = teacher_data.get("employment_status", "PRESENT").strip().upper()

        return insert_teacher(connection, teacher_id, teacher_name, designation, department,
                       email, phone, address, joining_year, employment_status)
        
    except Exception as e:
        print(f"❌ Error in teacher_info(): {e}")
    finally:
        connection.close()
