import datetime
import os
import json
import event_patterns
import database_connection
import businesslogic
import cx_Oracle
import time
import datetime
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask_cors import CORS
from flask import Flask, jsonify, request
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
        original_file_path = event.src_path

        try:
            # Delay to allow file write completion
            time.sleep(1)

            with open(original_file_path, 'r') as file:
                file_content = file.read()
                file_id = businesslogic.generate_file_id(file_content)
                logger.info(f"Generated file ID: {file_id} for file: {original_file_path}")

            # Rename the file with the new file ID
            new_file_name = f'{file_id}.txt'
            new_file_path = os.path.join(os.path.dirname(original_file_path), new_file_name)
            os.rename(original_file_path, new_file_path)
            logger.info(f"Renamed {original_file_path} to {new_file_path}")
            logger.info(f"Current contents of the archive directory: {os.listdir(archive_directory)}")
            # Check if the file with the new ID already exists in the archive
            archived_file_path = os.path.join(archive_directory, new_file_name)
            print(f"Checking if file exists: {archived_file_path}")
            if os.path.isfile(archived_file_path):
                logger.info(f"File with ID {file_id} already exists in archive. Deleting file {new_file_path}.")
                os.remove(new_file_path)
                return
            
               
            shutil.move(new_file_path, archive_directory)
            logger.info(f"Moved {new_file_path} to {archive_directory}")

            result = process_file(archived_file_path, file_id, new_file_name)
            processed_files.append({'file_id': file_id, 'file_name': new_file_name, 'file_path': archived_file_path, 'result': json.loads(result)})

            with open(results_json_file, 'w') as json_file:
                json.dump(processed_files, json_file, indent=4)
                logger.info(f"Updated results JSON file with data from {new_file_name}")

        except Exception as e:
            logger.error(f"Error processing file {original_file_path}: {e}", exc_info=True)


def process_file(file_path, file_id, file_name):
    processed_files=[]
    try:
        with open(file_path, 'r') as file:
            text = file.read()

        event_blocks = businesslogic.extract_event_blocks(text)
        results = []

        with database_connection.get_connection() as connection:
            logger.info("Connected to Oracle Database")


            for block in event_blocks:
                system_data = businesslogic.extract_system_info(block)
                event_id = system_data.get('EventID')
                event_data = businesslogic.extract_event_data(block, event_id) if event_id else {}
                concordance_data = businesslogic.extract_concordance_data(block)
                results.append({'System': system_data, 'EventData': event_data, 'Concordance': concordance_data, 'FileID': file_id, 'FileName': file_name})

                params=None
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


     
                if params:
                    database_connection.insert_into_assets(connection, params.get('asset_name'), params.get('ip_addr'), params.get('asset_type'), registration_date_formatted)
                    database_connection.insert_into_users(connection,params.get('asset_name'))   
                    database_connection.insert_into_events(connection,event_id,params.get('event_type'),params.get('description'),params.get('asset_name'),params.get('asset_name'))
                    database_connection.insert_into_log_files(connection,file_id,file_name,file_path)
                    database_connection.insert_into_log_activity(connection,file_id,event_id,registration_date_formatted,params.get('asset_name'),params.get('asset_name'),params.get('asset_name'))
                else:
                    database_connection.insert_into_log_files(connection,file_id,file_name,file_path)
                for word, occurrences in concordance_data.items():
                    for occurrence in occurrences:
                        row_num, word_num = occurrence
                     
                        print(f"Inserting into concordance: word Name: {word}, file id: {file_id}, rownum: {row_num}, wordnum Date: {word_num}")

                        database_connection.insert_into_concordance(connection, word, file_id, row_num, word_num)

        logger.info("Database connection released back to pool")
        
        return json.dumps(results, indent=4)

    except cx_Oracle.Error as e:
        logger.error("Database error: %s", e)
        raise
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
