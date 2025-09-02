"""
Lokesh Muvva - MSDS692 HW1 Streamlit
"""


import pickle

import pandas as pd
import requests
import streamlit as st

from user_definition import role_name, url_list, company_dictionary


def retrieve_data_from_urls(urls: list) -> list:
    """
    Read data from url_list and return
    a list of unique dictionaries
    which includes all the data from url in url_list.
    """
    all_jobs = []

    for url in urls:
        r = requests.get(url)
        data = pickle.loads(r.content)
        all_jobs.extend(data)

    df_jobs = pd.DataFrame(all_jobs)
    df_unique = df_jobs.drop_duplicates()
    return df_unique.to_dict("records")


def filter_by_company(data: pd.DataFrame,
                      company_dict: dict) -> pd.DataFrame:
    """
    For the given data (data frame) and company_dictionary,
    create checkboxes and return a new dataframe
    which only includes data being checked.
    """
    st.sidebar.markdown("Filter by Company")

    selected_companies = []
    with st.sidebar:
        for company in company_dict:
            if st.checkbox(company):
                selected_companies.append(company)

    if len(selected_companies) == 0:
        return pd.DataFrame()

    filtered_companies = pd.DataFrame()
    for company in selected_companies:
        substring_link = company_dict[company]
        link_matches = data[data["link"].str.contains(substring_link,
                                                      case=False,
                                                      na=False,
                                                      regex=False)]
        filtered_companies = pd.concat([filtered_companies,
                                        link_matches]).drop_duplicates()
    return filtered_companies


if __name__ == '__main__':
    st.title(f"{role_name} Job Listings")
    jobs_list = retrieve_data_from_urls(url_list)
    df = pd.DataFrame(jobs_list)
    filtered_df = filter_by_company(df, company_dictionary)

    if filtered_df.empty:
        display_df = pd.DataFrame(columns=["date", "title", "link"])
    else:
        display_df = filtered_df[["date", "title", "link"]]

    st.dataframe(
        display_df,
        column_config={"link": st.column_config.LinkColumn("Link")}
        )
