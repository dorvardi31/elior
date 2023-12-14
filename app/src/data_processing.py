import datetime
import os
import json
import re
import event_patterns
import database_connection
import businesslogic
import cx_Oracle
import hashlib
import time
import datetime
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask_cors import CORS
from flask import Flask
import logging
import sys
from datetime import datetime


app = Flask(__name__)
CORS(app)

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

input_directory = '/opt/input'

archive_directory = '/opt/archive'


results_json_file = './json/results.json'
result_json_directory ='./json/'
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        logger.info(f"New file detected: {event.src_path}")
        if event.is_directory:
            logger.info(f"Directory created: {event.src_path}, ignoring...")
            return
        file_path = event.src_path

        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
                file_id = generate_file_id(file_content)
                logger.info(f"Generated file ID: {file_id} for file: {file_path}")

            archived_file_name = f'{file_id}.txt'
            archived_file_path = os.path.join(archive_directory, archived_file_name)
            shutil.move(file_path, archived_file_path)
            logger.info(f"Moved {file_path} to {archived_file_path}")

            result = process_file(archived_file_path, file_id, archived_file_name)
            processed_files.append({'file_id': file_id, 'file_name': archived_file_name,'file_path': archived_file_path, 'result': json.loads(result)})

            with open(results_json_file, 'w') as json_file:
                json.dump(processed_files, json_file, indent=4)
                logger.info(f"Updated results JSON file with data from {archived_file_name}")

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}", exc_info=True)

def generate_file_id(file_content):
    try:
        file_hash = hashlib.sha256(file_content.encode()).hexdigest()
        return file_hash
    except Exception as e:
        logger.error(f"Error generating file ID: {e}", exc_info=True)
        return None

def extract_event_data(text, event_id):
    event_data = {}
    try:
        patterns_to_use = event_patterns.event_data_patterns_4624 if event_id == "4624" else {}

        for key, pattern in patterns_to_use.items():
            match = re.search(pattern, text)
            if match:
                event_data[key] = match.group(1).strip()

        return event_data

    except Exception as e:
        logger.error(f"Error extracting event data: {e}", exc_info=True)
        return {}

def extract_event_blocks(text):
    try:
        event_blocks = re.split(r'Event End', text)
        return [block.strip() for block in event_blocks if block.strip()]
    except Exception as e:
        logger.error(f"Error extracting event blocks: {e}", exc_info=True)
        return []

def process_file(file_path, file_id, file_name):
    try:
        with open(file_path, 'r') as file:
            text = file.read()

        event_blocks = extract_event_blocks(text)
        results = []

        connection = None
        try: 
            dsnStr = cx_Oracle.makedsn("db", database_connection.PORT, service_name=database_connection.SERVICE_NAME)
            connection = cx_Oracle.connect(user=database_connection.USERNAME, password=database_connection.PASSWORD, dsn=dsnStr)
            logger.info("Connected to Oracle Database")


            for block in event_blocks:
                system_data = businesslogic.extract_system_info(block)
                event_id = system_data.get('EventID')
                event_data = extract_event_data(block, event_id) if event_id else {}
                concordance_data = businesslogic.extract_concordance_data(block)
                results.append({'System': system_data, 'EventData': event_data, 'Concordance': concordance_data, 'FileID': file_id, 'FileName': file_name})

                if event_id in event_patterns.event_id_to_preparation:
                    params = event_patterns.event_id_to_preparation[event_id](event_data, system_data, file_id, file_name)
    
                asset_name = event_data.get('LogonAccountName')
                ip_addr = event_data.get('Source Network Address')
                asset_type = event_data.get('Logon Type')
                registration_date_str = system_data.get('DateAndTime')
                try:
                    registration_date_obj = datetime.strptime(registration_date_str, '%m/%d/%Y %I:%M:%S %p')
                    registration_date_formatted = registration_date_obj.strftime('%d-%b-%Y %H:%M:%S')

                    
                except ValueError as e:
                    logger.error(f"Error parsing date: {e}")
                    registration_date_formatted = None  


     
                print(f"Inserting into assets: Asset Name: {asset_name}, IP Address: {ip_addr}, Asset Type: {asset_type}, Registration Date: {registration_date_formatted}")

       
                database_connection.insert_into_assets(connection, params.get('asset_name'), params.get('ip_addr'), params.get('asset_type'), params.get('registration_date_formatted'))
                database_connection.insert_into_users(connection,params.get('asset_name'))
                database_connection.insert_into_log_files(connection,file_id,file_name,file_path)
                database_connection.insert_into_events(connection,event_id,params.get('event_type'),params.get('description'),params.get('asset_name'),params.get('asset_name'))
                for word, occurrences in concordance_data.items():
                    for occurrence in occurrences:
                        row_num, word_num = occurrence
                     
                        print(f"Inserting into concordance: word Name: {word}, file id: {file_id}, rownum: {row_num}, wordnum Date: {word_num}")

                        database_connection.insert_into_concordance(connection, word, file_id, row_num, word_num)


        finally:
            if connection:
                connection.close()
                logger.info("Database connection closed")

        return json.dumps(results, indent=4)

    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}", exc_info=True)
        return json.dumps([])

if __name__ == "__main__":
    processed_files = []  

    try:
        if not os.path.exists(input_directory):
            os.makedirs(input_directory)
            logger.info(f"Created input directory: {input_directory}")

        if not os.path.exists(archive_directory):
            os.makedirs(archive_directory)
            logger.info(f"Created archive directory: {archive_directory}")

        if not os.path.exists(result_json_directory):
            os.makedirs(result_json_directory)
            logger.info(f"Created result json directory: {result_json_directory}")    

        

        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, path=input_directory, recursive=False)
        observer.start()
        logger.info("Started observer for directory monitoring")

        while True:
            time.sleep(5)

    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        logger.info("Stopped observer and exiting application")

    except Exception as e:
        logger.error(f"Error in main application: {e}", exc_info=True)
