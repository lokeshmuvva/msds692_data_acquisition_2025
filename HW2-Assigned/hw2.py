import json

from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st
import pandas as pd

from user_definition import *


def retrieve_data_from_gcs(service_account_key: str,
                           project_id: str,
                           bucket_name: str,
                           file_name_prefix: str
                           ) -> dict:
    """
    Retrieve file contents from all files starting with 'file_name_prefix'
    in "bucket_name" and returns a dictionary including "results",
    "job_titles", and"company_dict"

    Args:
        service_account_key (str) : path of service account key file(.json)
        project_id (str) : GCP Project ID where bucket is located
        bucket_name (str) : bucket name
        file_name_prefix (str) : prefix of files to retrieve data.
                                 (Ex."job_search/")

    Returns:
        dict: in a following format
            {"results": a list including "results" from all the files
                        starting with file_name_prefix,
             "job_titles": a list including unique "job_title"s
                           from all the files starting with file_name_prefix,
             "company_dict": a dictionary including all "company_dict"s
                            from all the files starting with file_name_prefix
            }
    """
    try:
        # Create credentials from service account file
        credentials = service_account.Credentials.from_service_account_file(
            service_account_key
        )

        # Create storage client
        client = storage.Client(project=project_id, credentials=credentials)

        # Get bucket
        bucket = client.bucket(bucket_name)

        # List all blobs with the specified prefix
        blobs = bucket.list_blobs(prefix=file_name_prefix)

        all_results = []
        all_job_titles = set()
        all_company_dicts = {}

        # Process each file
        for blob in blobs:
            if blob.name.endswith('.json'):
                try:
                    # Download blob content
                    content = blob.download_as_text()
                    data = json.loads(content)

                    # Extract results
                    if 'results' in data:
                        all_results.extend(data['results'])

                    # Extract job titles
                    if 'job_title' in data:
                        all_job_titles.add(data['job_title'])

                    # Extract company dictionaries
                    if 'company_dict' in data:
                        all_company_dicts.update(data['company_dict'])

                except json.JSONDecodeError:
                    continue

        return {
            "results": all_results,
            "job_titles": sorted(list(all_job_titles)),
            "company_dict": all_company_dicts
        }

    except Exception as e:
        st.error(f"Error retrieving data from GCS: {e}")
        return {
            "results": [],
            "job_titles": [],
            "company_dict": {}
        }


if __name__ == '__main__':
    # Title should be comma separated strings of job titles in ascending order.
    # Company list on the side bar should include unique names
    # in ascending order.
    # The dataframe should be filtered based on the selection on the sidebar.
    # The dataframe should only include unique values.
    # The dataframe should have date, title, and link columns where link
    # should be a hyperlink.

    try:
        gcs_data = retrieve_data_from_gcs(service_account_file_path,
                                          project_id,
                                          bucket_name,
                                          file_name_prefix)

        # Set up the page title with job titles (comma-separated, ascending)
        if gcs_data["job_titles"]:
            TITLE = ", ".join(gcs_data["job_titles"])
        else:
            TITLE = "Job Postings"

        st.title(TITLE)

        # Get unique company names and sort them in ascending order
        if gcs_data["company_dict"]:
            company_list = sorted(list(gcs_data["company_dict"].keys()))
        else:
            company_list = []

        # Create sidebar for company filtering (similar to HW1 approach)
        st.sidebar.markdown("Filter by Company")

        selected_companies = []
        with st.sidebar:
            for company in company_list:
                if st.checkbox(company):
                    selected_companies.append(company)

        # If no companies selected, show empty dataframe
        if len(selected_companies) == 0:
            display_df = pd.DataFrame(columns=["date", "title", "link"])
        else:
            # Convert results to DataFrame and remove duplicates
            if gcs_data["results"]:
                df = pd.DataFrame(gcs_data["results"])
                df = df.drop_duplicates()

                # Filter by selected companies (similar to HW1 logic)
                filtered_df = pd.DataFrame()
                for company in selected_companies:
                    if company in gcs_data["company_dict"]:
                        company_url = gcs_data["company_dict"][company]
                        # Extract domain from company URL for matching
                        domain = company_url.replace('https://', '')\
                            .replace('http://', '').split('/')[0]
                        link_matches = df[df["link"].str.contains(domain,
                                                                  case=False,
                                                                  na=False,
                                                                  regex=False)]
                        filtered_df = pd.concat([filtered_df,
                                                link_matches])\
                            .drop_duplicates()

                # Select only the required columns
                if not filtered_df.empty:
                    display_df = filtered_df[["date",
                                              "title",
                                              "link"]]
                else:
                    display_df = pd.DataFrame(columns=["date",
                                                       "title",
                                                       "link"])
            else:
                display_df = pd.DataFrame(columns=["date",
                                                   "title",
                                                   "link"])

        # Display the dataframe with clickable links (same as HW1)
        st.dataframe(
            display_df,
            column_config={"link": st.column_config.LinkColumn("Link")}
        )

    except Exception as e:
        st.error(f"Error loading application: {e}")
