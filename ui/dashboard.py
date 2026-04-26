import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import streamlit as st
import json
import pandas as pd
from datetime import datetime
from module.visualization import show_category_pie_chart, show_monthly_trend_line, show_category_bar_chart
from module.expenses_manager import ExpenseManager
# ------------------ APP CONFIG ------------------ #
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💰 Expense Tracker Dashboard")

# ------------------ INIT MANAGER ------------------ #
manager = ExpenseManager()

# ------------------ SIDEBAR: ADD EXPENSE ------------------ #
st.sidebar.header("➕ Add Expense")

amount = st.sidebar.number_input("Amount", min_value=0.0, step=1.0)
category = st.sidebar.selectbox("Category", manager.get_categories() or ["Other"])
date = st.sidebar.date_input("Date", datetime.today())
note = st.sidebar.text_input("Note")

if st.sidebar.button("Add Expense"):
    try:
        if amount <= 0:
            st.sidebar.error("Amount must be greater than 0")
        else:
            manager.add_expense(amount, category, str(date), note)
            st.sidebar.success("Expense added successfully!")
            st.rerun()
    except Exception as e:
        st.sidebar.error(str(e))

# ------------------ LOAD DATA ------------------ #
data = manager.get_all_expenses()
df = pd.DataFrame(data)

# ------------------ MAIN DASHBOARD ------------------ #
st.subheader("📊 Overview")

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])

    # ------------------ METRICS ------------------ #
    total_spent = manager.get_total_expense()
    st.metric("Total Spending", f"₹ {total_spent:.2f}")

    st.subheader("📊 Analytics & Insights")
    col1, col2 = st.columns(2)
    with col1:
        show_category_pie_chart(df)
    with col2:
        show_category_bar_chart(df)
        
    show_monthly_trend_line(df)
    # ---------------------------------

    # ------------------ FILTER ------------------ #
    selected_category = st.selectbox(
        "Filter by Category",
        ["All"] + list(df["category"].unique())
    )

    if selected_category != "All":
        df = df[df["category"] == selected_category]

    # ------------------ TABLE ------------------ #
    st.subheader("📋 Expense Records")
    st.dataframe(df, use_container_width=True)

    # ------------------ EXPORT FUNCTION ------------------ #
    def export_csv(dataframe):
        os.makedirs("reports", exist_ok=True)
        filename = f"reports/expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        dataframe.to_csv(filename, index=False)
        return filename

    # ------------------ EXPORT BUTTON ------------------ #
    if st.button("📥 Export as CSV"):
        file_path = export_csv(df)
        st.success(f"Exported successfully to: {file_path}")

else:
    st.info("No expenses added yet. Start by adding one from the sidebar 👈")