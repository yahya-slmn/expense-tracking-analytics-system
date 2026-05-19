import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import calendar

API_URL = "http://localhost:8000"


def analytics_months_tab():
    st.title("Expense Breakdown By Months")
    responses = requests.get(f"{API_URL}/analytics_by_months/")

    if responses.status_code == 200:
        response = responses.json()
        # st.write(response)
    else:
        st.error("No expense data available")

    data = {
        "Month Name": [calendar.month_name[item["month"]] for item in response],
        "Total": [item["total_expense"] for item in response]
    }

    df = pd.DataFrame(data)
    chart_df = df.copy()  # keep numbers
    df.index = [item["month"] for item in response]
    df["Total"] = df["Total"].map("{:.2f}".format)

    st.bar_chart(data=chart_df.set_index("Month Name")['Total'], use_container_width=True)

    st.table(df)