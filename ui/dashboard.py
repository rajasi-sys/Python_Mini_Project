import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
from datetime import datetime
from module.visualization import show_category_pie_chart, show_monthly_trend_line, show_category_bar_chart
from module.expenses_manager import ExpenseManager
from module.auth import AuthManager

# ------------------ APP CONFIG ------------------ #
st.set_page_config(page_title="Expense Tracker", layout="wide")

# ------------------ SESSION INIT ------------------ #
# We store the authentication state so Streamlit remembers it between clicks
if "auth" not in st.session_state:
    st.session_state.auth = AuthManager()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ------------------ AUTHENTICATION WALL ------------------ #
if not st.session_state.logged_in:
    st.title("🔐 Welcome to Expense Tracker")
    
    # Create tabs for Login and Sign up
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login to your account")
        log_user = st.text_input("Username", key="log_user")
        log_pass = st.text_input("Password", type="password", key="log_pass")
        
        if st.button("Login"):
            try:
                if st.session_state.auth.login(log_user, log_pass):
                    st.session_state.logged_in = True
                    st.session_state.username = log_user
                    st.rerun() # Refresh the page to load the dashboard
            except ValueError as e:
                st.error(str(e))
                
    with tab2:
        st.subheader("Create a new account")
        sign_user = st.text_input("New Username", key="sign_user")
        sign_pass = st.text_input("New Password", type="password", key="sign_pass")
        
        if st.button("Sign Up"):
            try:
                if st.session_state.auth.signup(sign_user, sign_pass):
                    st.success("Account created successfully! You can now log in.")
            except ValueError as e:
                st.error(str(e))
                
    # VERY IMPORTANT: Stop execution here if not logged in!
    st.stop()


# ==============================================================================
# ------------------ MAIN DASHBOARD (Only visible if logged in) ----------------
# ==============================================================================

st.title(f"💰 {st.session_state.username}'s Dashboard")

# ------------------ INIT MANAGER ------------------ #
# We dynamically set the file path so each user gets their own JSON file!
user_file = f"data/expenses_{st.session_state.username}.json"
manager = ExpenseManager(file_path=user_file)

# ------------------ SIDEBAR ------------------ #
st.sidebar.header(f"👤 Welcome, {st.session_state.username}!")

if st.sidebar.button("Logout"):
    st.session_state.auth.logout()
    st.session_state.logged_in = False
    del st.session_state.username
    st.rerun()

st.sidebar.divider()

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

# ------------------ MAIN OVERVIEW ------------------ #
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
        # We also added the username to the export file name!
        filename = f"reports/{st.session_state.username}_expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        dataframe.to_csv(filename, index=False)
        return filename

    # ------------------ EXPORT BUTTON ------------------ #
    if st.button("📥 Export as CSV"):
        file_path = export_csv(df)
        st.success(f"Exported successfully to: {file_path}")

else:
    st.info("No expenses added yet. Start by adding one from the sidebar 👈")