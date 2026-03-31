import Logics.database_connector as database_connector

def get_institutional_emails(input_email):
    try:
        connection = database_connector.connect_to_db("admin_interface")
        if not connection:
            return {"is_valid": False, "reason": "Database connection failed"}

        cursor = connection.cursor()
        query = '''
            SELECT Institute_Email
            FROM id_pass
        '''
        cursor.execute(query)
        emails = cursor.fetchall()

        if any(input_email == email_tuple[0] for email_tuple in emails):
            return False
        
    except Exception as e:
        print(f"An error occurred while fetching emails in EMAIL_EXISTANCE: {e}")
        return {"is_valid": False, "reason": "Error during database query"}
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

