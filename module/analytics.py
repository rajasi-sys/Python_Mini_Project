import pandas as pd

def get_total_spending(df):
    """Calculates the total spending from the dataframe."""
    if df.empty:
        return 0.0
    return df["amount"].sum()

def get_spending_by_category(df):
    """Groups expenses by category and sums the amounts."""
    if df.empty:
        return pd.DataFrame(columns=["category", "amount"])
    
    # Group by category and sum the amounts, returning a clean dataframe
    return df.groupby("category", as_index=False)["amount"].sum()

def get_monthly_trend(df):
    """Calculates total spending per month to show trends."""
    if df.empty:
        return pd.DataFrame(columns=["month", "amount"])
    
    # Create a copy to avoid modifying the original dataframe warnings
    df_trend = df.copy()
    
    # Ensure the date column is a datetime object
    df_trend["date"] = pd.to_datetime(df_trend["date"])
    
    # Extract just the Year and Month (e.g., "2026-04")
    df_trend["month"] = df_trend["date"].dt.strftime('%Y-%m')
    
    # Group by the new month column
    return df_trend.groupby("month", as_index=False)["amount"].sum()

def get_top_category(df):
    """Identifies the category with the highest spending."""
    if df.empty:
        return "None", 0.0
    
    cat_df = get_spending_by_category(df)
    
    # Find the row with the maximum amount
    top_row = cat_df.loc[cat_df["amount"].idxmax()]
    return top_row["category"], top_row["amount"]