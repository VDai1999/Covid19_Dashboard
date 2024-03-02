import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import timedelta

import warnings
warnings.filterwarnings("ignore")

from utils import table_display


def page1():
    # Directory to a folder that stores data
    saved_data_pth = "data"

    # Read data us
    us = pd.read_csv(f"{saved_data_pth}/us.csv")
    us['date'] = pd.to_datetime(us['date'])

    # Start date and end date to filter
    start_date = pd.to_datetime(us["date"]).min()
    end_date = pd.to_datetime(us["date"]).max()

    selected_date = pd.to_datetime(st.date_input("**Start Date**", value=end_date, min_value=start_date, max_value=end_date))

    # Filter US data to match date range that users choose
    us = us[us["date"] == selected_date]
    us.reset_index(drop=True, inplace=True)

    # Add CSS styles to highlight the box
    st.markdown(
        """
        <style>
        .highlight {
            border: 2px solid #f0ad4e;
            border-radius: 5px;
            padding: 10px;
            background-color: #fcf8e3;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div><br></div>", unsafe_allow_html=True)

    col1, col2 = st.columns((2))
    total_cases = us.at[0, 'cases']
    total_cases = "{:,}".format(total_cases)
    total_deaths = us.at[0, 'deaths']
    total_deaths = "{:,}".format(total_deaths)
    daily_cases = us.at[0, 'daily_cases']
    daily_cases = "{:,}".format(daily_cases)
    daily_deaths = us.at[0, 'daily_deaths']
    daily_deaths = "{:,}".format(daily_deaths)
    with col1:
        st.markdown(f'<div class="highlight"><i class="fas fa-virus"></i><b>TOTAL CASES:</b> {total_cases}</div><br>', unsafe_allow_html=True)
        st.markdown(f'<div class="highlight"><b>DAILY CASES:</b> {daily_cases}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="highlight"><b>TOTAL DEATHS:</b> {total_deaths}</div><br>', unsafe_allow_html=True)
        st.markdown(f'<div class="highlight"><b>DAILY DEATHS:</b> {daily_deaths}</div>', unsafe_allow_html=True)


    st.markdown("<div><br></div>", unsafe_allow_html=True)

    # Display radio buttons
    option = st.radio(
        "**Select a number to view the top # states**",
        ["5", "10", "15"]
    )

    # Display the DataFrame as a table
    states = pd.read_csv(f"{saved_data_pth}/states.csv")
    states['Date'] = pd.to_datetime(states['Date'])
    states = states[states["Date"] == selected_date]
    states.reset_index(drop=True, inplace=True)

    col1_1, col2_1 = st.columns((2))
    with col1_1:
        # Top # of states by total cases
        table_display(
            df=states,
            column="Total_Cases",
            column_rename="Total Cases",
            option=option,
        )

        # Top # of states by total cases
        table_display(
            df=states,
            column="daily_cases",
            column_rename="Daily Cases",
            option=option,
        )

    with col2_1:
        # Top # of states by total deaths
        table_display(
            df=states,
            column="Total_Deaths",
            column_rename="Total Deaths",
            option=option,
        )

        # Top # of states by total cases
        table_display(
            df=states,
            column="daily_deaths",
            column_rename="Daily Deaths",
            option=option,
        )