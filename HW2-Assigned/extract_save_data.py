import datetime
import json
import re

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google.oauth2 import service_account
from google.cloud import storage
from pydantic import BaseModel
import requests

from user_definition import *

app = FastAPI()


class GoogleSearch(BaseModel):
    url: str  # GoogleAPI URLs Ex. "https://www.googleapis.com/customsearch/v1"
    search_engine_id: str  # Google API's customsearch engine id
    # GCP API Key (different from service account key
    # this is for custom search)
    api_key: str
    no_days: int  # For the search restuls
    job_title: str
    company_dictionary: dict


class GcsStringUpload(BaseModel):
    service_account_key: str
    project_id: str
    bucket_name: str
    file_name: str
    data: str


@app.post("/search/jobs")
def call_google_search(search_param: GoogleSearch):
    """
    Refer to https://developers.google.com/custom-search/v1/reference/rest/v1/Search
    parameters should be properly assigned including
    key, cx, query, and dateRestrict, etc.
    If the search returns more than 100 matches, it should limit the matches 
    to 100.
    """
    # Create search query using job titles and company sites
    company_sites = " OR ".join([f"site:{url}" for url in
                                search_param.company_dictionary.values()])
    query = f"{search_param.job_title} ({company_sites})"

    # Setting up parameters for Google Custom Search API
    params = {
        'key': search_param.api_key,
        'cx': search_param.search_engine_id,
        'q': query,
        'dateRestrict': f'd{search_param.no_days}',
        'num': 10
    }

    all_results = []
    start_index = 1

    # Get up to 100 results only
    while len(all_results) < 100 and start_index <= 91:
        params['start'] = start_index

        try:
            response = requests.get(search_param.url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'items' not in data:
                break

            for item in data['items']:
                if len(all_results) >= 100:
                    break

                # Extract date
                snippet = item.get('snippet', '')
                date_match = re.search(r'(\d+)\s+days?\s+ago', snippet)

                if date_match:
                    days_ago = int(date_match.group(1))
                    job_date = (date.today() - timedelta(days=days_ago))\
                        .strftime('%Y-%m-%d')
                else:
                    job_date = date.today().strftime('%Y-%m-%d')

                result = {
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': snippet,
                    'date': job_date
                }
                all_results.append(result)

            # If we got fewer than 10 results, we've reached the end
            if len(data.get('items', [])) < 10:
                break

            start_index += 10

        except Exception as e:
            print(f"Error fetching search results: {e}")
            break

    return {
        "company_dict": search_param.company_dictionary,
        "job_title": search_param.job_title,
        "results": all_results
    }


@app.put("/save_to_gcs")
def save_to_gcs(gcs_upload_param: GcsStringUpload):
    """
    Access the bucket with service_account_key, and upload the object(blob)
    the the storage.
    It should return a dictionary of message.
    """
    try:
        # Get credentials from service account file
        credentials = service_account.Credentials.from_service_account_file(
            gcs_upload_param.service_account_key
        )

        # Using storage.Client
        client = storage.Client(
            project=gcs_upload_param.project_id,
            credentials=credentials
        )

        # Using the bucket function
        bucket = client.bucket(gcs_upload_param.bucket_name)

        # Using blob function and uploading data
        blob = bucket.blob(gcs_upload_param.file_name)
        blob.upload_from_string(gcs_upload_param.data,
                                content_type='application/json')

        return {"message": f"file {gcs_upload_param.file_name} has been "
                          f"uploaded to {gcs_upload_param.bucket_name} "
                          f"successfully."}

    except Exception as e:
        return {"error": f"Failed to upload file: {str(e)}"}
