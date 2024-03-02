import streamlit as st
import plotly.express as px
import pandas as pd
import warnings

from urllib.request import urlopen
import json

from datetime import timedelta

warnings.filterwarnings("ignore")

from utils import line_plot

def page2():
    # Directory to a folder that stores data
    saved_data_pth = "data"

    # Read data us
    us = pd.read_csv(f"{saved_data_pth}/us.csv")
    us['date'] = pd.to_datetime(us['date'])

    # Start date and end date to filter
    start_date = pd.to_datetime(us["date"]).min()
    end_date = pd.to_datetime(us["date"]).max()

    # Display the start date and end date calendar to filter
    col1, col2 = st.columns((2))
    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", start_date))
    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", end_date))

    # Filter US data to match date range that users choose
    us = us[(us["date"] >= date1) & (us["date"] <= date2)].copy()


    ###############################
    ## TOTAL DAILY CASES PLOT
    ###############################
    with col1:
        line_plot(
            df=us,
            header="Total Daily Cases",
            x_axis="date",
            y_axis="daily_cases",
            x_axis_label="Date",
            y_axis_label="Number of Cases")


    ###############################
    ## DAILY NEW CASES PLOT
    ###############################
    with col2:
        us['new_daily_cases'] = us['daily_cases'].diff().fillna(us['daily_cases'])
        us['new_daily_cases'] = us['new_daily_cases'].apply(lambda x: max(0, x))
        line_plot(
            df=us,
            header="Daily New Cases",
            x_axis="date",
            y_axis="new_daily_cases",
            x_axis_label="Date",
            y_axis_label="Number of Cases")


    ##############################################
    ## TOTAL HOSPITALIZATION PATIENTS PLOT
    ##############################################
    hos = pd.read_csv(f"{saved_data_pth}/COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries__RAW__20240228.csv")
    # Columns to keep
    cols = ['state', 
            'date',
            'previous_day_admission_adult_covid_confirmed_18-19',
            'previous_day_admission_adult_covid_confirmed_20-29',
            'previous_day_admission_adult_covid_confirmed_30-39',
            'previous_day_admission_adult_covid_confirmed_40-49',
            'previous_day_admission_adult_covid_confirmed_50-59',
            'previous_day_admission_adult_covid_confirmed_60-69',
            'previous_day_admission_adult_covid_confirmed_70-79',
            'previous_day_admission_adult_covid_confirmed_80+',
            'previous_day_admission_adult_covid_confirmed_unknown',
            'critical_staffing_shortage_today_yes'
            ]
    hos = hos[cols]

    # Sort the data by date and state
    hos.sort_values(by=['date', 'state'], inplace=True)
    hos.reset_index(drop=True, inplace=True)

    # Create an admission day column for the admission columns
    hos["date"] = pd.to_datetime(hos["date"])
    hos["admission_date"] = hos["date"] - timedelta(days=1)

    # Rename columns
    column_mapping = {
        "previous_day_admission_adult_covid_confirmed_18-19": "admission_18-19",
        "previous_day_admission_adult_covid_confirmed_20-29": "admission_20-29",
        "previous_day_admission_adult_covid_confirmed_30-39": "admission_30-39",
        "previous_day_admission_adult_covid_confirmed_40-49": "admission_40-49",
        "previous_day_admission_adult_covid_confirmed_50-59": "admission_50-59",
        "previous_day_admission_adult_covid_confirmed_60-69": "admission_60-69",
        "previous_day_admission_adult_covid_confirmed_70-79": "admission_70-79",
        "previous_day_admission_adult_covid_confirmed_80+": "admission_80+",
        "previous_day_admission_adult_covid_confirmed_unknown": "admission_unknown",
        "critical_staffing_shortage_today_yes": "num_hospital_shortage_staff"
    }
    hos = hos.rename(columns=column_mapping)

    hos_summary = hos[['admission_18-19', 'admission_20-29',
        'admission_30-39', 'admission_40-49', 'admission_50-59',
        'admission_60-69', 'admission_70-79', 'admission_80+',
        'admission_unknown', 'admission_date']].groupby('admission_date').sum().reset_index()
    hos_summary = pd.melt(hos_summary, id_vars=['admission_date'], var_name="age_group", value_name="new_hospitalization_cases")

    # Change the values
    value_mapping = {
        'admission_18-19': "18 to 19",
        'admission_20-29': "20 to 29",
        'admission_30-39': "30 to 39",
        'admission_40-49': "40 to 49",
        'admission_50-59': "50 to 59",
        'admission_60-69': "60 to 69",
        'admission_70-79': "70 to 79",
        'admission_80+': "80+",
        'admission_unknown': "unknown"
    }
    hos_summary["age_group"] = hos_summary['age_group'].replace(value_mapping)
    hos_summary = hos_summary[(hos_summary["admission_date"] >= date1) & (hos_summary["admission_date"] <= date2)]

    st.subheader("Total Number of Hospital Admissions by Age")
    fig = px.line(hos_summary, x='admission_date', y='new_hospitalization_cases', color="age_group")
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Number of Hospitalization Cases')
    # fig.update_traces(hovertemplate=
    #                     'Age Group: %{legendgroup}<br>' + 
    #                     'Date: %{x}<br>' + 
    #                     'Hospitalization Cases: %{y}')
    for trace in fig.data:
        trace.hovertemplate = (
            'Age Group: ' + trace.name + '<br>' +
            'Date: %{x}<br>' + 
            'Hospitalization Cases: %{y:,}'
        )
    st.plotly_chart(fig)


    ######################################################################
    ## COMPARISON OF HOSPITALIZATION CASES OF US VERSUS OTHER COUNTRIES
    ######################################################################
    world_hos = pd.read_csv(f"{saved_data_pth}/current-covid-patients-hospital.csv")
    world_hos["Day"] = pd.to_datetime(world_hos["Day"])
    
    # Get country lists
    countries = world_hos['Entity'].unique().tolist()
    countries.remove("United States")

    selected_countries = st.multiselect(
        '**Select countries to compare to the U.S**',
        countries,
        ["Australia"])
    
    world_hos = world_hos[(world_hos["Day"] >= date1) & (world_hos["Day"] <= date2) & (world_hos['Entity'].isin(["United States"] + selected_countries))].copy()
    st.subheader("Number of COVID-19 Patients in Hospital of the U.S versus Other Countries")
    fig = px.line(world_hos, x='Day', y='Daily hospital occupancy', color="Entity")
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Number of Hospitalization Cases')
    # fig.update_traces(hovertemplate=
    #                     'Age Group: %{legendgroup}<br>' + 
    #                     'Date: %{x}<br>' + 
    #                     'Hospitalization Cases: %{y}')
    for trace in fig.data:
        trace.hovertemplate = (
            'Country: ' + trace.name + '<br>' +
            'Date: %{x}<br>' + 
            'Hospitalization Cases: %{y:,}'
        )
    st.plotly_chart(fig)


    ########################################################################################
    ## MAP THAT SHOWS THE SHORTAGE OF STAFFS IN HOSPITAL ACROSS DIFFERENT STATES IN THE US
    ########################################################################################
    st.subheader("Number of Staff Shortages in Hospitals")
    start_date = pd.to_datetime(us["date"]).min()
    end_date = pd.to_datetime(us["date"]).max()

    # Filter date
    selected_date = pd.to_datetime(st.date_input("**Start Date**", value=end_date, min_value=start_date, max_value=end_date))
    hos = hos[hos['date'] == selected_date].copy()
    hos.reset_index(drop=True, inplace=True)
        
    # Mapping dictionary for state abbreviations to full names
    state_mapping = {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming'
    }

    # Map state abbreviations to full names
    hos['state_full'] = hos['state'].map(state_mapping)

    fig = px.choropleth(
        hos, locations='state', color='num_hospital_shortage_staff',
        locationmode="USA-states",
        color_continuous_scale="blues",
        range_color=(0, max(hos.num_hospital_shortage_staff)),
        scope="usa",
        labels={'num_hospital_shortage_staff':'Number of Shortage Staffs'}
    )
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    st.plotly_chart(fig)