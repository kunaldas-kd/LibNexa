# from getmac import get_mac_address
import Logics.database_connector as database_connector
# import database_connector

def storemac(USER_Id):
    # Get MAC address
    mac = 1
    
    # Connect to the database
    connection = database_connector.connect_to_db(f"{USER_Id}_library_db")
    if not connection:
        print("Database connection failed.")
        return False

    cursor = connection.cursor()
    try:
        # Update the MAC Address for the given USER_Id
        student_query = '''
            UPDATE users 
            SET `MAC Address` = %s 
            WHERE Id = %s
        '''
        cursor.execute(student_query, (mac, USER_Id))

        # Commit changes
        connection.commit()

        print(f"MAC Address {mac} stored successfully for user ID {USER_Id}.")
        return True

    except Exception as e:
        print("Error occurred:", e)
        return False

    # finally:
    #     # Clean up
    #     cursor.close()
    #     connection.close()

# storemac("949028")
def autosignin():
    # Step 1: Connect to the database server
    connection = database_connector.connect_to_db("")
    if not connection:
        print(" Database connection failed.")
        return False

    cursor = connection.cursor()

    # Step 2: Get all databases ending with "_library_db"
    try:
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall() if db[0].endswith('_library_db')]
    except Exception as e:
        print(f"Failed to fetch databases: {e}")
        return False

    # Step 3: Search for matching MAC address in each database
    for db in databases:
        # try:
        cursor.execute(f"USE `{db}`")
        cursor.execute("SELECT Id, Passwords FROM users WHERE `MAC Address` = %s", (1,))
        results = cursor.fetchone()
        print(results)
    try:
        if results:
            Id, password = results
            print(f"Auto-signed in from {db}: ID={Id}")
            return Id, password
        else:
            print(f"No user found with MAC in {db}")
            return False
    except Exception as e:
        print(f"⚠️ Error accessing {db}: {e}")
        # continue

    # print("❌ MAC address not found in any '_library_db' database.")
    # return False


# autosignin()

def clearmac(USER_Id):
    connection = database_connector.connect_to_db(f"{USER_Id}_library_db")
    if not connection:
        print("Database connection failed.")
        return False

    cursor = connection.cursor()
    try:
        update_query = '''
            UPDATE users
            SET `MAC Address` = NULL
            WHERE Id = %s
        '''
        cursor.execute(update_query, (USER_Id,))
        connection.commit()
        print(f"MAC Address cleared for student ID {USER_Id}.")
        return True
    except Exception as e:
        print("Error occurred:", e)
        return False
    # finally:
    #     cursor.close()
    #     connection.close()



# clearmac(949028)