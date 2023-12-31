import cx_Oracle
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

USERNAME = 'SYSTEM'
PASSWORD = 'Sep2023N'
HOST = 'oracle_db'  # Replace with the actual hostname or IP address
PORT = '1521'
SERVICE_NAME = 'XEPDB1'
CONNECTION_STRING = f'{USERNAME}/{PASSWORD}@{HOST}:{PORT}/{SERVICE_NAME}'

# Function to create a database connection using a context manager
def create_db_connection():
    try:
        dsnStr = cx_Oracle.makedsn("db", PORT, service_name=SERVICE_NAME)
        connection = cx_Oracle.connect(user=USERNAME, password=PASSWORD, dsn=dsnStr)
            
        logger.info("Database connection created successfully")
        return connection
    except cx_Oracle.Error as e:
        logger.error(f"Database connection error: {str(e)}")
        raise e

# Function to execute SQL queries using a context manager
def execute_sql(connection, sql, params=None):
    try:
        with connection.cursor() as cursor:
            logger.info(f"SQL Query Executed: {sql}, Params: {params}")
            logger.info(f"Database Connection: {connection}")

            # Execute the SQL query with parameters
            if params is not None:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

            logger.info(f"SQL Query Result: {result}")
            return result
    except cx_Oracle.Error as e:
        logger.error(f"Oracle Error: {str(e)}")
        raise e


# Example usage:
if __name__ == "__main__":
    with create_db_connection() as connection:
        sql_query = "SELECT * FROM combined_data_view"
        result = execute_sql(connection, sql_query)
        # Process the query result
