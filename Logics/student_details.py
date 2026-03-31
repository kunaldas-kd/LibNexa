import Logics.database_connector as database_connector

def get_student_details(student_id, db_name):
    """Fetches student details from the Students table based on Student_ID."""
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("Failed to connect to MySQL.")
        return None

    cursor = connection.cursor()
    try:
        query = """
            SELECT Student_ID, Student_Name, Student_Email, Department
            FROM Students
            WHERE Student_ID = %s
        """
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        if result:
            student_details = {
                "Student_ID": result[0],
                "Student_Name": result[1],
                "Student_Email": result[2],
                "Department": result[3]
            }
            print(f"Student Details: {student_details}")
            return student_details
        else:
            print(f"No student found with Student_ID {student_id}.")
            return None
    except Exception as e:
        print(f"Error fetching student details in student details: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
