import streamlit as st
import data_processing
import page1, page2

# Process data
data_processing.main()

# Layout for the app
st.set_page_config(page_title="Covid-19 Dashboard", page_icon=":us:", layout="wide")

st.title(" :flag-us: US Covid-19 Dashboard")
st.markdown("<style>div.block-container{padding-top:1rem}</style>", unsafe_allow_html=True)

# Navigation buttons
nav_option = st.radio('Go to', ['Summary Statistics', 'Visualisations'], index=0)

if nav_option == 'Summary Statistics':
    page1.page1()
elif nav_option == 'Visualisations':
    page2.page2()