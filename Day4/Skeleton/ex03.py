"""
Module for fetching SF police data and storing it to Google Cloud Storage.
"""
import datetime
import json
import os
import requests

from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import storage


def store_to_gcs(service_account_key_path: str,
                 project_id: str,
                 bucket_name: str,
                 file_name: str,
                 data: str) -> None:
    """
    Store data to Google Cloud Storage.

    Args:
        service_account_key_path: Path to service account key file
        project_id: GCP project ID
        bucket_name: GCS bucket name
        file_name: Name of file to store
        data: Data to store as string
    """
    credentials = service_account.Credentials.from_service_account_file(
        service_account_key_path)
    client = storage.Client(project=project_id,
                            credentials=credentials)
    bucket = client.bucket(bucket_name)
    file = bucket.blob(file_name)
    file.upload_from_string(data)


def get_json_response(api_url: str, api_key: str):
    """
    Get JSON response from API endpoint.

    Args:
        api_url: URL to fetch data from
        api_key: API key for authentication

    Returns:
        JSON response from API
    """
    header = {'X-Api-Key': api_key}
    response = requests.get(api_url, headers=header, timeout=30)
    return response.json()


if __name__ == '__main__':
    load_dotenv(
        dotenv_path='/Users/lokeshmuvva/'
        'Documents/msds692_data_acquisition_2025/Day3/.env'
    )
    data_gov_api_key = os.getenv("DATA_GOV_API_KEY")
    genai_api_key = os.getenv("GCP_GENAI_API_KEY")
    service_account_key = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
    project_id = os.getenv("GCP_PROJECT_ID")
    bucket_name = os.getenv("GCP_BUCKET_NAME")
    FILE_NAME = f"sf_police_report/{datetime.date.today()}.json"
    URL = 'https://data.sfgov.org/resource/wg3w-h783'
    data = get_json_response(URL, data_gov_api_key)
    store_to_gcs(service_account_key,
                 project_id,
                 bucket_name,
                 FILE_NAME,
                 json.dumps(data, indent=4))
