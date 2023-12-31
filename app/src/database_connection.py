import cx_Oracle

USERNAME = 'SYSTEM'
PASSWORD = 'Sep2023N'   
HOST = '127.0.0.1'
PORT = '1521'
SERVICE_NAME = 'XEPDB1'
CONNECTION_STRING = f'{USERNAME}/{PASSWORD}@{HOST}:{PORT}/{SERVICE_NAME}'



def insert_into_assets(connection, asset_name, ip_addr, asset_type, registration_date):
    cursor = connection.cursor()
    try:

        sql_check = "SELECT COUNT(*) FROM assets WHERE asset_name = :1"
        cursor.execute(sql_check, (asset_name,))
        if cursor.fetchone()[0] == 0:
      
            sql_insert = """
            INSERT INTO assets (asset_name, ip_addr, type, registration_date) 
            VALUES (:1, :2, :3, TO_DATE(:4, 'DD-MON-YYYY HH24:MI:SS'))
            """
            cursor.execute(sql_insert, (asset_name, ip_addr, asset_type, registration_date))
            connection.commit()
            print("Data inserted into assets table successfully.")
        else:
            print("Asset already exists, skipping insertion.")
    except cx_Oracle.Error as error:
        print("Error inserting data into assets table:", error)
    finally:
        cursor.close()

def insert_into_concordance(connection, word, file_id, row_num, word_num):
    cursor = connection.cursor()
    try:
        # Check if the record already exists
        check_sql = """
        SELECT COUNT(*) FROM concordance
        WHERE word = :1 AND file_id = :2 AND row_num = :3 AND word_num = :4
        """
        cursor.execute(check_sql, (word, file_id, row_num, word_num))
        (count,) = cursor.fetchone()

        # If count is 0, the record does not exist; proceed with insertion
        if count == 0:
            insert_sql = """
            INSERT INTO concordance (word, file_id, row_num, word_num, groups)
            VALUES (:1, :2, :3, :4, :5)
            """
            cursor.execute(insert_sql, (word, file_id, row_num, word_num, None))
            connection.commit()
            print("Data inserted into concordance table successfully.")
        else:
            print("Duplicate record found. Skipping insertion.")

    except cx_Oracle.Error as error:
        print("Error in operation with concordance table:", error)
    finally:
        cursor.close()






def insert_into_users(connection, username):
    cursor = connection.cursor()
    try:
      
        sql_check = "SELECT COUNT(*) FROM users WHERE username = :1"
        cursor.execute(sql_check, (username,))
        result = cursor.fetchone()
        if result[0] == 0:
  
            sql_insert = "INSERT INTO users (username, registration_date) VALUES (:1, SYSDATE)"
            cursor.execute(sql_insert, (username,))
            connection.commit()
            print("Data inserted into users table successfully.")
        else:
            print("User already exists, skipping insertion.")
    except cx_Oracle.Error as error:
        print("Error in insert_into_users function:", error)
    finally:
        cursor.close()
        print("Database connection closed")


def insert_into_events(connection, event_id, event_type, description, username_regex, evidence_regex):
    cursor = connection.cursor()
    try:

        sql_check = "SELECT COUNT(*) FROM events WHERE event_id = :1"
        cursor.execute(sql_check, (event_id,))
        result = cursor.fetchone()
        if result[0] == 0:
 
            sql_insert = "INSERT INTO events (event_id, event_type, description, username_regex, evidence_regex) VALUES (:1, :2, :3, :4, :5)"
            cursor.execute(sql_insert, (event_id, event_type, description, username_regex, evidence_regex))
            connection.commit()
            print("Data inserted into events table successfully.")
        else:
            print("Event already exists, skipping insertion.")
    except cx_Oracle.Error as error:
        print("Error inserting data into events table:", error)
    finally:
        cursor.close()
        print("Database connection closed")


def insert_into_log_files(connection, file_id, file_name, file_path):
    cursor = connection.cursor()
    try:

        sql_check = "SELECT COUNT(*) FROM log_files WHERE file_id = :1"
        cursor.execute(sql_check, (file_id,))
        result = cursor.fetchone()
        if result[0] == 0:

            sql_insert = "INSERT INTO log_files (file_id, file_name, file_path) VALUES (:1, :2, :3)"
            cursor.execute(sql_insert, (file_id, file_name, file_path))
            connection.commit()
            print("Data inserted into log_files table successfully.")
        else:
            print("Log file already exists, skipping insertion.")
    except cx_Oracle.Error as error:
        print("Error inserting data into log_files table:", error)
    finally:
        cursor.close()
        print("Database connection closed")




def insert_into_log_activity(connection, file_id, event_id, event_time, asset_name, username, evidence):
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO log_activity ( file_id, event_id, event_time, asset_name, username, evidence) " \
              "VALUES (:1, :2,TO_DATE(:3,'DD-MON-YYYY HH24:MI:SS'), :4, :5, :6)"
        cursor.execute(sql, ( file_id, event_id, event_time, asset_name, username, evidence))
        connection.commit()
        print("Data inserted into log_activity table successfully.")
    except cx_Oracle.Error as error:
        print("Error inserting data into log_activity table:", error)
    finally:
        cursor.close()
        print("Database connection closed")



