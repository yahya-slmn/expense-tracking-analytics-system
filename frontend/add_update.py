import streamlit as st
from datetime import datetime
import pandas as pd
import os

DATA_PATH = os.path.join("data", "sample_expenses.csv")

def load_data():
    return pd.read_csv(DATA_PATH)

def save_data(df):
    df.to_csv(DATA_PATH, index=False)

def add_update_tab():
    selected_date = st.date_input(
        "Enter Date",
        datetime(2024, 8, 1),
        label_visibility="collapsed"
    )

    df = load_data()

    selected_date_str = selected_date.strftime("%Y-%m-%d")

    existing_expenses = df[df["expense_date"] == selected_date_str].to_dict("records")

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Transport", "Other"]

    with st.form(key="expense_form"):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.text("Amount")

        with col2:
            st.text("Category")

        with col3:
            st.text("Notes")

        expenses = []

        for i in range(5):

            if i < len(existing_expenses):
                amount = existing_expenses[i]["amount"]
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)

            with col1:
                amount_input = st.number_input(
                    "Amount",
                    min_value=0.0,
                    step=1.0,
                    value=float(amount),
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )

            with col2:
                category_input = st.selectbox(
                    "Category",
                    options=categories,
                    index=categories.index(category),
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )

            with col3:
                notes_input = st.text_input(
                    "Notes",
                    value=notes,
                    key=f"notes_{i}",
                    label_visibility="collapsed"
                )

            if amount_input > 0:
                expenses.append({
                    "expense_date": selected_date_str,
                    "amount": amount_input,
                    "category": category_input,
                    "notes": notes_input
                })

        submit_button = st.form_submit_button("Save Expenses")

        if submit_button:

            df = df[df["expense_date"] != selected_date_str]

            new_df = pd.DataFrame(expenses)

            updated_df = pd.concat([df, new_df], ignore_index=True)

            save_data(updated_df)

            st.success("Expenses updated successfully!")