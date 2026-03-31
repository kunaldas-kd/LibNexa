import Logics.database_connector as database_connector

def get_input(ip):
    validinput = input(ip).strip().capitalize()
    while not validinput:
        print("You must fill it.")
        validinput = input(ip).strip().capitalize()
    validinput = validinput.upper()
    return validinput

def get_user_email_by_id(id):
    try:
        connection = database_connector.connect_to_db('Admin_Interface')
        if connection is None:
            return None, None

        cursor = connection.cursor()
        query = "SELECT Institute_Email, Passwords FROM id_pass WHERE Id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if result:
            return result[0], result[1] 
        else:
            return None, None
    except Exception as e:
        print(f"Error retrieving user email in input_module(get_user_email_by_id): {e}")
        return None, None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def sendpass(email):
    try:
        connection = database_connector.connect_to_db('Admin_Interface')
        if connection is None:
            return None, None

        cursor = connection.cursor()
        query = "SELECT Id, Passwords FROM id_pass WHERE Institute_Email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result:
            return result[0], result[1]   
        else:
            return False
    except Exception as e:
        print(f"Error retrieving user email in sendpass: {e}")
        return None, None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if connection and connection.is_connected():
            connection.close()