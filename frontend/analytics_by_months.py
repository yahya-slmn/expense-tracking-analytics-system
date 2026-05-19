import streamlit as st
import pandas as pd
import calendar
import os

DATA_PATH = os.path.join("data", "sample_expenses.csv")

def analytics_months_tab():

    st.title("Expense Breakdown By Months")

    df = pd.read_csv(DATA_PATH)

    df["expense_date"] = pd.to_datetime(df["expense_date"])

    df["month"] = df["expense_date"].dt.month

    grouped = df.groupby("month")["amount"].sum().reset_index()

    grouped["Month Name"] = grouped["month"].apply(lambda x: calendar.month_name[x])

    chart_df = grouped.copy()

    grouped["amount"] = grouped["amount"].map("{:.2f}".format)

    st.bar_chart(
        chart_df.set_index("Month Name")["amount"],
        use_container_width=True
    )

    grouped.columns = ["Month", "Total", "Month Name"]

    st.table(grouped[["Month Name", "Total"]])