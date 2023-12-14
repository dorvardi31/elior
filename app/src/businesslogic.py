import nltk
from nltk.corpus import stopwords
import re
import json
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def extract_concordance_data(text):
    concordance = {}
    for row_num, line in enumerate(text.split('\n'), start=1):
        words = line.split()
        for word_num, word in enumerate(words, start=1):
            word = re.sub(r'[^\w\s]', '', word).lower()  # Removing punctuation and converting to lowercase
            if word and word not in stop_words:
                if word not in concordance:
                    concordance[word] = []
                concordance[word].append((row_num, word_num))
    return concordance

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
