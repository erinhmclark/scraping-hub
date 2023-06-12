""" This module provides functions for authenticating with and interacting with Google Sheets.
"""
import uuid
import csv
from typing import List
import pandas as pd
import gspread
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime


def authenticate_with_service_account(service_account_file: str) -> gspread.Client:
    """
    Authenticate with a service account JSON.
    """
    return gspread.service_account(filename=service_account_file)


def authenticate_with_installed_app(client_secrets_file: str) -> gspread.Client:
    """
    Authenticate with an installed app client secrets JSON file.
    """
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    creds = flow.run_local_server(port=0)
    return gspread.authorize(creds)


def authenticate_with_oauth2(creds: credentials.Credentials) -> gspread.Client:
    """
    Authenticate with OAuth2 credentials.
    """
    return gspread.authorize(creds)


def check_for_headers(worksheet: gspread.Worksheet, headers: List[str]) -> None:
    """
    Check for headers in the worksheet and add them if they do not exist.
    """
    existing_headers = worksheet.row_values(1)
    if existing_headers != headers:
        if not existing_headers:
            worksheet.append_row(headers)
        else:
            raise ValueError("Existing headers do not match the provided data headers.")


def insert_from_dict(sheet_id: str, sheet_name: str, data: dict, client: gspread.Client):
    """
    Insert a single row of data into a Google Sheet using a dictionary where the key is the column name
    and the value is the row value.
    """
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(sheet_name)

    headers = ["unique_id", "date_inserted"] + list(data.keys())
    check_for_headers(worksheet, headers)

    # Create a data list with unique_id, date_inserted, and values from the input dictionary
    data_list = [str(uuid.uuid4()), datetime.now().strftime('%Y-%m-%d %H:%M:%S')] + list(data.values())
    worksheet.append_row(data_list)


def insert_data_from_json(sheet_id: str, sheet_name: str, data: dict, client: gspread.Client):
    """
    Insert data into a Google Sheet from a JSON-like structure where the keys are row identifiers,
    and the values are dictionaries with column names as keys and row values as values.
    """
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(sheet_name)

    headers = ["unique_id", "date_inserted"] + list(next(iter(data.values())).keys())
    check_for_headers(worksheet, headers)

    # Create a data list with unique_id, date_inserted, and values from the input JSON structure
    data_list = [
        [str(uuid.uuid4()), datetime.now().strftime('%Y-%m-%d %H:%M:%S')] + list(row.values())
        for row in data.values()
    ]

    for row in data_list:
        worksheet.append_row(row)


def insert_from_dataframe(sheet_id: str, sheet_name: str, df: pd.DataFrame, client: gspread.Client):
    """
    Insert or update a Google Sheet with a pandas DataFrame.
    """

    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(sheet_name)

    headers = ["unique_id", "date_inserted"] + list(df.columns)
    check_for_headers(worksheet, headers)

    data_list = []
    for _, row in df.iterrows():
        unique_id = str(uuid.uuid4())
        date_inserted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_list.append([unique_id, date_inserted] + list(row))

    for row in data_list:
        worksheet.append_row(row)


def read_sheet_to_csv(sheet_id: str, sheet_name: str, client: gspread.Client, output_file: str):
    """
    Read a Google Sheet and save it as a CSV file.
    """
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(sheet_name)

    data = worksheet.get_all_values()

    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)
