import streamlit as st
import plotly.express as px
import pandas as pd
import warnings
from datetime import timedelta
warnings.filterwarnings("ignore")

def line_plot(
        df: pd.DataFrame,
        header: str,
        x_axis: str,
        y_axis: str,
        x_axis_label: str,
        y_axis_label: str    
    ):
    st.subheader(header)
    fig = px.line(df, x=x_axis, y=y_axis)
    fig.update_xaxes(title_text=x_axis_label)
    fig.update_yaxes(title_text=y_axis_label)
    fig.update_traces(hovertemplate='Date: %{x}<br>' + 'Number of Cases: %{y:,}')
    st.plotly_chart(fig)


def table_display(
        df: pd.DataFrame,
        column: str,
        column_rename: str,
        option: int,
        width: int = 1_000,
    ):
    df_ = df[["State", column]].copy()
    df_.sort_values(by=column, ascending=False, inplace=True)
    df_.reset_index(drop=True, inplace=True)
    df_.index += 1
    df_.rename(columns={column: column_rename}, inplace=True)
    st.dataframe(df_.iloc[:int(option), :], width=width)