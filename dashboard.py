import streamlit as st
import page1, page2

# Layout for the app
st.set_page_config(page_title="Covid-19 Dashboard", page_icon=":us:", layout="wide")

st.title(" :flag-us: US Covid-19 Dashboard")
st.markdown("<style>div.block-container{padding-top:1rem}</style>", unsafe_allow_html=True)

# Navigation buttons
nav_option = st.radio('Go to', ['Page 1', 'Page 2'], index=0)

if nav_option == 'Page 1':
    page1.page1()
elif nav_option == 'Page 2':
    page2.page2()
