import streamlit as st
import plotly.express as px
from module.analytics import get_spending_by_category, get_monthly_trend

def show_category_pie_chart(df):
    """Displays a donut chart of spending by category."""
    cat_df = get_spending_by_category(df)
    
    if not cat_df.empty:
        fig = px.pie(
            cat_df, 
            values='amount', 
            names='category', 
            title='Spending Distribution by Category', 
            hole=0.4, # Makes it a donut chart for a modern look
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        # Render the chart directly in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add some expenses to see the category breakdown.")

def show_monthly_trend_line(df):
    """Displays a line graph showing spending trends over time."""
    trend_df = get_monthly_trend(df)
    
    if not trend_df.empty:
        fig = px.line(
            trend_df, 
            x='month', 
            y='amount', 
            title='Monthly Spending Trend', 
            markers=True
        )
        # Customize the layout for better readability
        fig.update_layout(xaxis_title="Month", yaxis_title="Amount")
        st.plotly_chart(fig, use_container_width=True)

def show_category_bar_chart(df):
    """Displays a bar chart comparing category totals."""
    cat_df = get_spending_by_category(df)
    
    if not cat_df.empty:
        fig = px.bar(
            cat_df, 
            x='category', 
            y='amount', 
            color='category', 
            title='Category Comparison',
            text_auto='.2s' # Automatically adds the values on top of the bars
        )
        st.plotly_chart(fig, use_container_width=True)
