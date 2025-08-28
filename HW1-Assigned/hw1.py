import pickle

import pandas as pd
import requests
import streamlit as st

from user_definition import *


def retrieve_data_from_urls(url_list: list) -> list:
    """
    Read data from url_list and return
    a list of unique dictionaries
    which includes all the data from url in url_list.
    """


def filter_by_company(data: pd.DataFrame, company_dictionary: dict)\
        -> pd.DataFrame:
    """
    For the given data (data frame) and company_dictionary,
    create checkboxes and return a new dataframe
    which only includes data being checked.
    """


if __name__ == '__main__':