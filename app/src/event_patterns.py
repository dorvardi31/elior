from datetime import datetime
import logging
def prepare_data_for_event_4624(event_data, system_data, file_id, file_name):

    registration_date_str = system_data.get('DateAndTime')
    try:
        registration_date_obj = datetime.strptime(registration_date_str, '%m/%d/%Y %I:%M:%S %p')
        registration_date_formatted = registration_date_obj.strftime('%d-%b-%Y %H:%M:%S')
    except ValueError as e:
        logging.Logger.error(f"Error parsing date: {e}")
        registration_date_formatted = None


    return {
        "asset_name": event_data.get('LogonAccountName'),
        "ip_addr": event_data.get('Source Network Address'),
        "asset_type": event_data.get('Logon Type'),
        "registration_date": registration_date_formatted,
        "file_id": file_id,
        "file_name": file_name,
        "event_id": system_data.get('EventID'),
        "event_type": system_data.get('TaskCategory'),
        "description":system_data.get('Description'),
        "evidence": event_data.get('LogonAccountName')

    }


event_data_patterns_4624 = {
    'Security ID': r'Security ID:\s+([^\n]+)',
    'Account Name': r'Account Name:\s+([^\n]+)',
    'Account Domain': r'Account Domain:\s+([^\n]+)',
    'Logon Type': r'Logon Type:\s+([^\n]+)',
    'Restricted Admin Mode': r'Restricted Admin Mode:\s+([^\n]+)',
    'Virtual Account': r'Virtual Account:\s+([^\n]+)',
    'Elevated Token': r'Elevated Token:\s+([^\n]+)',
    'Impersonation Level': r'Impersonation Level:\s+([^\n]+)',
    'LogonSecurityID' :r'New Logon:\n\s+Security ID:\s+([^\n]+)\n',
    'LogonAccountName' :r'New Logon:\n\s+Security ID:\s+[^\n]+\n\s+Account Name:\s+([^\n]+)\n',
    'LogonDomainName' :r'New Logon:\n\s+Account Domain:\s+([^\n]+)\n',
    'Logon ID': r'Logon ID:\s+([^\n]+)',
    'Linked Logon ID': r'Linked Logon ID:\s+([^\n]+)',
    'NetworkAccountName' :r'New Logon:\n\s+Network Account Name:\s+([^\n]+)\n',
    'NetworkAccountDomain' :r'New Logon:\n\s+Network Account Domain:\s+([^\n]+)\n',
    'Logon GUID': r'Logon GUID:\s+([^\n]+)',
    'Process ID': r'Process ID:\s+([^\n]+)',
    'Process Name': r'Process Name:\s+([^\n]+)',
    'Workstation Name': r'Workstation Name:\s+([^\n]+)',
    'Source Network Address': r'Source Network Address:\s+([^\n]+)',
    'Source Port': r'Source Port:\s+([^\n]+)',
    'Logon Process': r'Logon Process:\s+([^\n]+)',
    'Authentication Package': r'Authentication Package:\s+([^\n]+)',
    'Transited Services': r'Transited Services:\s+([^\n]+)',
    'Package Name (NTLM only)': r'Package Name \(NTLM only\):\s+([^\n]+)',
    'Key Length': r'Key Length:\s+([^\n]+)',
    'Subject': r'Subject:\n\s+Security ID:\s+([^\n]+)\n\s+Account Name:\s+([^\n]+)\n\s+Account Domain:\s+([^\n]+)\n\s+Logon ID:\s+([^\n]+)',
    'Logon Information': r'Logon Information:\n\s+Logon Type:\s+([^\n]+)\n\s+Restricted Admin Mode:\s+([^\n]+)\n\s+Virtual Account:\s+([^\n]+)\n\s+Elevated Token:\s+([^\n]+)',
    'New Logon': r'New Logon:\n\s+Security ID:\s+([^\n]+)\n\s+Account Name:\s+([^\n]+)\n\s+Account Domain:\s+([^\n]+)\n\s+Logon ID:\s+([^\n]+)\n\s+Linked Logon ID:\s+([^\n]+)\n\s+Network Account Name:\s+([^\n]+)\n\s+Network Account Domain:\s+([^\n]+)\n\s+Logon GUID:\s+([^\n]+)',
}

event_data_pattern = {
    '4624': event_data_patterns_4624,

}


event_id_to_preparation = {
    '4624': prepare_data_for_event_4624,

}

