import pandas as pd
import numpy as np
# from datetime import datetime
# import requests

import altair as alt
from vega_datasets import data
import plotly.express as px

def main():
    # Data URLs
    us_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    states_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    regions_url = "https://raw.githubusercontent.com/cphalpert/census-regions/master/us%20census%20bureau%20regions%20and%20divisions.csv"

    # Read Data
    us = pd.read_csv(us_url)
    states = pd.read_csv(states_url)
    regions = pd.read_csv(regions_url)

    saved_data_pth = "data"

    ## REGIONAL DATA
    regions_extra = pd.DataFrame({
        'State': ["Puerto Rico", "Virgin Islands", "Guam", "Northern Mariana Islands"],
        'State.Code': ["RR", "VI", "GU", "MP"],
        'Region': ["Other", "Other", "Other", "Other"],
        'Division': ["None", "None", "None", "None"]
    })

    regions = pd.concat([regions, regions_extra])

    # Save data
    regions.to_csv(f"{saved_data_pth}/regions.csv", index=False)


    ## STATE DATA
    # Change the date column from character format to date format and state column from character to factor format
    states['date'] = pd.to_datetime(states['date'])

    # Check to see if we calculate the right daily cases and daily deaths
    states['daily_cases'] = states.groupby('state')['cases'].diff().fillna(states['cases'])
    states['daily_deaths'] = states.groupby('state')['deaths'].diff().fillna(states['deaths'])

    # Merge the Region column to states dataframe
    states = pd.merge(states, regions[['State', 'Region']], left_on='state', right_on='State', how='left')
    states['Region'] = pd.Categorical(states['Region'], categories=["Northeast", "Midwest", "West", "South", "Other"], ordered=True)
    states.drop(columns=["State"], inplace=True)

    # Rename variables
    states = states.rename(columns={'state': 'State', 'date': 'Date', 'cases': 'Total_Cases', 'deaths': 'Total_Deaths'})

    # Save data
    states.to_csv(f"{saved_data_pth}/states.csv", index=False)


    ## US DATA
    # Change the date column from character format to date format
    us['date'] = pd.to_datetime(us['date'])

    # Calculate the daily cases and daily deaths
    us['daily_cases'] = np.concatenate(([us['cases'].iloc[0]], np.diff(us['cases'])))
    us['daily_deaths'] = np.concatenate(([us['deaths'].iloc[0]], np.diff(us['deaths'])))

    # Save data
    us.to_csv(f"{saved_data_pth}/us.csv", index=False)


if __name__ == "__main__":
    main()