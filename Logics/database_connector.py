import mysql.connector

def connect_to_db(database=None):
    """Connects to MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin@123',
            # password='Kunaldas05032001#',
            # password='ashim007@',
            database=database
        ) 
        if connection.is_connected():
            # print("Successfully connected to the database")
            return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    
# connect_to_db('admin_interface')