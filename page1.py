import streamlit as st
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def page1():
    saved_data_pth = "data"
    us = pd.read_csv(f"{saved_data_pth}/us.csv")
    us['date'] = pd.to_datetime(us['date'])

    start_date = pd.to_datetime(us["date"]).min()
    end_date = pd.to_datetime(us["date"]).max()

    col1, col2 = st.columns((2))

    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", start_date))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", end_date))

    us = us[(us["date"] >= date1) & (us["date"] <= date2)].copy()

    st.subheader("Daily Cases")
    fig = px.line(us, x='date', y='daily_cases')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Daily Cases')
    st.plotly_chart(fig)

    # Daily New Case
    us['new_daily_cases'] = us['daily_cases'].diff().fillna(us['daily_cases'])
    us['new_daily_cases'] = us['new_daily_cases'].apply(lambda x: max(0, x))
    st.subheader("New Daily Cases")
    fig = px.line(us, x='date', y='new_daily_cases')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='New Daily Cases')
    st.plotly_chart(fig)

    # Plotly Express map
    fig = px.choropleth(us, 
                        locations='State', 
                        locationmode='USA-states', 
                        color='Total_Cases', 
                        scope='usa',
                        color_continuous_scale='blues',
                        labels={'Total_Cases':'Total Cases'}
                        )

    # Set layout properties
    fig.update_layout(
        title='COVID-19 Cases by State',
        geo=dict(
            lakecolor='rgb(255, 255, 255)',
            projection=dict(
                type='albers usa'
            )
        )
    )

    # Display the map in Streamlit
    st.plotly_chart(fig)


# st.set_page_config(page_title="Covid-19 Dashboard", page_icon=":us:", layout="wide")

# st.title(" :flag-us: US Covid-19 Dashboard")
# st.markdown("<style>div.block-container{padding-top:1rem}</style>", unsafe_allow_html=True)

# # fl = str.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
# # if fl is not None:
# #     filename = fl.name
# #     st.write(filename)
# #     df = pd.read_csv(filename)
# # else:
# #     os.cdir("")

# # Read data
# saved_data_pth = "data"
# df = pd.read_csv(f"{saved_data_pth}/states.csv")
# df["Date"] = pd.to_datetime(df['Date'])

# # Get the min and max date
# start_date = pd.to_datetime(df["Date"]).min()
# end_date = pd.to_datetime(df["Date"]).max()

# col1, col2 = st.columns((2))

# with col1:
#     date1 = pd.to_datetime(st.date_input("Start Date", start_date))

# with col2:
#     date2 = pd.to_datetime(st.date_input("End Date", end_date))

# df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()

# st.sidebar.header("Choose your filter: ")
# region = st.sidebar.multiselect("Pick your region", df["Region"].unique())
# if not region:
#     df2 = df.copy()
# else:
#     df2 = df[df["Region"].isin(region)]

# # Create for state
# state = st.sidebar.multiselect("Pick your state", df2["State"].unique())
# if not state:
#     df3 = df2.copy()
# else:
#     df3 = df2[df2["State"].isin(region)]


# # General line graph
# us = pd.read_csv(f"{saved_data_pth}/us.csv")
# us['date'] = pd.to_datetime(us['date'])

# st.subheader("Daily Cases")
# fig = px.line(us, x='date', y='daily_cases', title='Daily Cases')
# st.plotly_chart(fig)

# # Daily New Case
# us['new_daily_cases'] = us['daily_cases'].diff().fillna(us['daily_cases'])
# us['new_daily_cases'] = us['new_daily_cases'].apply(lambda x: max(0, x))
# st.subheader("Daily New Cases")
# fig = px.line(us, x='date', y='new_daily_cases', title='Daily New Cases')
# st.plotly_chart(fig)