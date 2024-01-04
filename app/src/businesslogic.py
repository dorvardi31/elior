import hashlib
import os
import shutil
import nltk
from nltk.corpus import stopwords
import re
import json
import logging
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import data_processing
import event_patterns
from collections import defaultdict


logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_concordance_data(text):
    concordance = defaultdict(list)
    for row_num, line in enumerate(text.split('\n'), start=1):
        words = line.split()

        for word_num, word in enumerate(words, start=1):
            cleaned_word = re.sub(r'[^\w\s]', '', word).lower()
            
            if cleaned_word:
                concordance[cleaned_word].append((row_num, word_num))

    return dict(concordance)

def extract_system_info(text):
    system_info = {}
    system_line_pattern = r'Keywords\tDate and Time\tSource\tEvent ID\tTask Category\n([^\n]+)'
    system_line_match = re.search(system_line_pattern, text)

    if system_line_match:
        system_line = system_line_match.group(1)
        parts = system_line.split('\t')
        system_info['Keywords'] = parts[0]
        system_info['DateAndTime'] = parts[1]
        system_info['Source'] = parts[2]
        system_info['EventID'] = parts[3]
        system_info['TaskCategory'] = parts[4]
        system_info['Description'] =parts[5]
    return system_info

def prepare_asset_data(event_data, system_data):
    # Extract data from the JSON
    logon_account_name = system_data.get('LogonAccountName')
    source_network_address = event_data.get('Source Network Address')
    logon_type = event_data.get('Logon Type')
    date_and_time = system_data.get('DateAndTime')

    return logon_account_name, source_network_address, logon_type, date_and_time





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
        patterns_to_use =   event_patterns.event_data_pattern[event_id] 
        if not patterns_to_use:
            #skip the extract
            return
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
        event_blocks = re.split(r'This event is generated', text)
        return [block.strip() for block in event_blocks if block.strip()]
    except Exception as e:
        logger.error(f"Error extracting event blocks: {e}", exc_info=True)
        return []
