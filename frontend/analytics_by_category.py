import streamlit as st
from datetime import datetime
import pandas as pd
import os

DATA_PATH = os.path.join("data", "sample_expenses.csv")

def analytics_category_tab():

    df = pd.read_csv(DATA_PATH)

    df["expense_date"] = pd.to_datetime(df["expense_date"])

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))

    with col2:
        end_date = st.date_input("End Date", datetime(2024, 9, 30))

    if st.button("Get Analytics"):

        filtered_df = df[
            (df["expense_date"] >= pd.to_datetime(start_date)) &
            (df["expense_date"] <= pd.to_datetime(end_date))
        ]

        grouped = filtered_df.groupby("category")["amount"].sum().reset_index()

        total_expense = grouped["amount"].sum()

        grouped["percentage"] = (grouped["amount"] / total_expense) * 100

        grouped = grouped.sort_values(by="percentage", ascending=False)

        st.title("Expense Breakdown By Category")

        st.bar_chart(
            grouped.set_index("category")["percentage"],
            use_container_width=True
        )

        grouped["amount"] = grouped["amount"].map("{:.2f}".format)
        grouped["percentage"] = grouped["percentage"].map("{:.2f}".format)

        grouped.columns = ["Category", "Total", "Percentage"]

        st.table(grouped)