import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

DATA_FILE= "data/expenses.json"        #path of file where expenses are stored

def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["amount", "category", "date", "note"])
    
    with open(DATA_FILE, "r") as f:
        data= json.load(f)    #reads json data and converts it to python list
        return pd.DataFrame(data)    #converts list to dataframe for easier manipulation(basically converts to a table)
    

def save_data(df):
    df.to_json(DATA_FILE, orient="records", indent=4)    #saves the dataframe back to json file, orient makes it readable by separating each entry and indent adds indentation for better readability


def add_expense(amount, caategory, date, note):
    df= load_data()    #loads existing data into dataframe
    new_entry= {"amount": amount, "category": caategory, "date": date, "note": note}    #creates a new entry as a dictionary

    df= df.concat([df, pd.DataFrame([new_entry])], ignore_index=True)    #concatenates the new entry to the existing dataframe, ignore_index resets the index after concatenation
    save_data(df)    #saves the updated dataframe back to json file


def export_csv(df):
    os.makedirs("reports", exist_ok=True)    #creates a directory named reports if it doesn't exist
    file_name= f"reports/expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"   #creates a filename with current date and time for uniqueness
    df.to_csv(file_name, index=False)    #saves the dataframe to a csv file without the index
    return file_name

#----UI Functions----
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💰 Expense Tracker Dashboard 💰 ")

st.sidebar.header("➕ Add New Expense")
amount= st.sidebar.number_input("Amount", min_value=0.0)
category = st.sidebar.selectbox( "Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health"])
date = st.sidebar.date_input("Date", datetime.today())   #datetime.today() gives current date and time from the user's system
note = st.sidebar.text_input("Note")

if st.sidebar.button("Add Expense"):
    add_expense(amount, category, date, note)
    st.sidebar.success("Expense added successfully!")

df = load_data()   #loads the data into a dataframe for display and manipulation

st.subheader("📊 Overview")

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])  #grouping the data by category and summing the amounts for each category, then sorting in descending order
    total = df["amount"].sum()
    st.metric("Total Spending", f"₹ {total:.2f}")

    selected_category = st.selectbox("Filter by Category", ["All"] + list(df["category"].unique()))  #creates a dropdown to filter the data by category, "All" option shows all data
    if selected_category != "All":
        df = df[df["category"] == selected_category]
    
    st.subheader("📋 Expense Records")
    st.dataframe(df)

    # Export button
    if st.button("📥 Export as CSV"):
        file = export_csv(df)
        st.success(f"Exported to {file}")

else:
    st.info("No expenses added yet.")


