import os
from decimal import Decimal

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Use BASE_DIR to ensure correct path resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Root directory of the project
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'sales', 'credentials.json')  # Path to the credentials.json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1xB20JwR0GU37i66zJnbLrBZXteWcoTGPlTtQ0hsaIbQ'
SHEET_NAME = 'Продажа'
SHEET_NAME1 = 'Диспетчер'

import logging
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


def append_to_sheet(data):
    """Append data to the Google Sheet starting explicitly from column B."""
    # Add an empty value to start in column B
    # data = [''] + data  # Add an empty string to shift data to column B

    #print(f"Appending data to Google Sheets: {data}")  # Debugging log

    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Use the entire row range to ensure placement in B onwards
        range_name = f'{SHEET_NAME}!A:K'  # A:K includes column A but skips filling it because of padding

        request = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            body={'values': [data]}
        )
        response = request.execute()
        #print(f"Google Sheets API Response: {response}")  # Debugging log
        return response
    except Exception as e:
        #print(f"Error in append_to_sheet: {e}")  # Error log
        raise




def get_dispatcher_names():
    """Fetch names from column H in Google Sheets and exclude the first actual data entry."""
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Fetch all data from column H
        range_name = f'{SHEET_NAME1}!H:H'
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()

        # Get the raw values
        values = result.get('values', [])
        #print(f"Fetched raw values from column H: {values}")  # Debugging

        # Exclude the first non-empty row
        filtered_values = [
            row[0] for row in values if row and row[0].strip()  # Remove empty rows
        ]
        #print(f"Filtered values before skipping first actual data: {filtered_values}")  # Debugging

        # Skip the first actual data entry
        if len(filtered_values) > 1:
            filtered_values = filtered_values[1:]  # Skip the first entry
        #print(f"Filtered values after skipping first actual data: {filtered_values}")  # Debugging

        return filtered_values
    except Exception as e:
        print(f"Error fetching dispatcher names: {e}")
        return []



def get_client_names():
    """Fetch names from column H in Google Sheets and exclude the first actual data entry."""
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Fetch all data from column H
        range_name = f'{SHEET_NAME1}!Q:Q'
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()

        # Get the raw values
        values = result.get('values', [])
        #print(f"Fetched raw values from column H: {values}")  # Debugging

        # Exclude the first non-empty row
        filtered_values = [
            row[0] for row in values if row and row[0].strip()  # Remove empty rows
        ]
        #print(f"Filtered values before skipping first actual data: {filtered_values}")  # Debugging

        # Skip the first actual data entry
        if len(filtered_values) > 1:
            filtered_values = filtered_values[1:]  # Skip the first entry
        #print(f"Filtered values after skipping first actual data: {filtered_values}")  # Debugging

        return filtered_values
    except Exception as e:
        print(f"Error fetching dispatcher names: {e}")
        return []

def get_car_numbers():
    """Fetch names from column H in Google Sheets and exclude the first actual data entry."""
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Fetch all data from column H
        range_name = f'{SHEET_NAME1}!R:R'
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()

        # Get the raw values
        values = result.get('values', [])
        #print(f"Fetched raw values from column H: {values}")  # Debugging

        # Exclude the first non-empty row
        filtered_values = [
            row[0] for row in values if row and row[0].strip()  # Remove empty rows
        ]
        #print(f"Filtered values before skipping first actual data: {filtered_values}")  # Debugging

        # Skip the first actual data entry
        if len(filtered_values) > 1:
            filtered_values = filtered_values[1:]  # Skip the first entry
        #print(f"Filtered values after skipping first actual data: {filtered_values}")  # Debugging

        return filtered_values
    except Exception as e:
        print(f"Error fetching dispatcher names: {e}")
        return []

