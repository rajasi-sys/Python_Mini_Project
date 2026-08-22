# Expense Tracker

A personal expense management web application built with **Python and Streamlit**. It allows users to securely manage expenses, analyze spending patterns, and export their records.

## Features

* User registration and login with password hashing and session-based authentication.
* Add, edit, delete, and filter expenses by category.
* Store user-specific expense data using JSON.
* View total spending and category-wise/monthly spending analytics.
* Interactive visualizations using Plotly.
* Export expense records as CSV.

## Tech Stack

* Python
* Streamlit
* Pandas
* Plotly
* JSON
* hashlib & UUID

## Project Structure

```text
Python_Mini_Project/
├── data/
├── module/
├── reports/
├── ui/
├── main.py
└── README.md
```

The project is organized into separate modules for authentication, expense management, analytics, visualization, and the user interface.

## Setup

### Requirements

* Python 3.9+
* pip

### Run

```bash
git clone https://github.com/rajasi-sys/Python_Mini_Project.git
cd Python_Mini_Project
pip install streamlit pandas plotly
python main.py
```

## Future Improvements

* Migrate from JSON to SQLite/PostgreSQL.
* Add budgets and spending alerts.
* Add date-range filtering and recurring expenses.
* Deploy the application online.
