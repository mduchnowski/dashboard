import pandas as pd
import json
import re
from datetime import datetime


#---For databasing
import sqlite3

#---For plots
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.figure_factory as ff
import plotly.subplots as sp

import streamlit as st
from streamlit_option_menu import option_menu 

st.set_page_config(layout="wide")


pio.templates.default="ggplot2"

# --- define constants
today = datetime.today().date()


from datetime import datetime, timedelta
import streamlit as st

# Function for finding how many days until payday 
@st.cache(suppress_st_warning=True)
def days_until_payday(date):
    # Get the current date
    today = datetime.today().date()

    # Get the day of the week (0 = Monday, 6 = Sunday)
    current_day = today.weekday()

    # Find the next Friday
    days_ahead = 4 - current_day  # 4 represents Friday
    if days_ahead < 0:
        days_ahead += 7
    next_friday = today + timedelta(days=days_ahead)

    # Calculate the number of days until the next payday
    days_until_payday = (next_friday - date).days

    return days_until_payday

# Function for finding how many days until payday 
@st.cache(suppress_st_warning=True)
def read_data_from_excel(workbook_name, sheet_name):
    try:
        df = pd.read_excel(".".join([workbook_name, "xlsx"]), sheet_name=sheet_name)
        return df
    except FileNotFoundError:
        print(f"File '{workbook_name}' not found.")
        return None
    except Exception as e:
        print("An error occurred while reading the Excel file.")
        print(e)
        return None

dfAllotment = read_data_from_excel("ledger","allotment")
dfEntries = read_data_from_excel("ledger", sheet_name="entries")

# Left join on 'Category' column and replace NaN with 0
df = dfAllotment.merge(dfEntries.groupby('Category')['Spent'].sum().reset_index(), on='Category', how='left').fillna(0)

# Set the desired sidebar width
sidebar_width = 100

# Define the custom CSS styles
custom_styles = """
<style>
.sidebar .sidebar-content {
    width: """ + str(sidebar_width) + """px;
}

.header-text {
    font-family: "Helvetica", Helvetica, sans-serif;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;  /* Adjust the margin bottom value */
}

.main-content {
    margin-top: -20px;  /* Adjust the margin top value */
}

tbody th {
    display: none;
}

.blank {
    display: none;
}
</style>
"""

# CSS styling
centered_style = '''
    <style>
    .centered-text {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        text-align: center;
    }
    </style>
    '''


# Apply the custom CSS styles using a single st.markdown call
st.markdown(custom_styles, unsafe_allow_html=True)

st.sidebar.markdown('<p class="header-text">Dashboard</p>', unsafe_allow_html=True)




#st.sidebar.header("Team Catalyst")

with st.sidebar:
        selected= option_menu(
            menu_title = None,
            options= ["Dashboard"],
            #menu_icon = "database",
            icons = ["activity"],
            default_index=0
        )
if selected == "Dashboard":
    #st.write(str(days_until_payday(datetime.today().date())))
    #st.dataframe(dfEntries)    
    #st.dataframe(dfAllotment)
    #st.dataframe(df)
    
    # Sample DataFrame
    #data = {
    #    'Category': ['Category A', 'Category B', 'Category C'],
    #    'Budget': [1000, 2000, 1500],
    #    'Spent': [600, 1200, 1000]
    #}
    #df = pd.DataFrame(data)

    # Calculate the percentage spent for each category
    df['Percentage Spent'] = df['Spent'] / df['Budget'] * 100

    # Create a single column using st.columns
    col0 = st.columns([100])

    
    
    # Display pie chart and bar chart for each category
    for _, row in df.iterrows():
        category = row['Category']
        budget = row['Budget'] 
        spent = row['Spent']
        percentage_spent = row['Percentage Spent']

        # Create a centered container for the title
        title_container = col0[0].container()
        with title_container:
            st.markdown('<div style="text-align:center"><h2>{}</h2></div>'.format(category), unsafe_allow_html=True)

        # Pie chart
        fig_pie = go.Figure(go.Pie(
            labels=['Spent', 'Remaining'],
            values=[spent, budget - spent],
            marker_colors=['blue', 'lightblue'],
            textinfo='label+percent',
            title=f'{category}<br>{percentage_spent:.2f}% Spent'
        ))
        fig_pie.update_layout(showlegend=False)

        # Bar chart
        fig_bar = go.Figure(go.Bar(
            x=['Spent'],
            y=[spent],
            marker_color=['blue', 'lightblue'],
            text=[spent, budget - spent],
            textposition='auto',
            hoverinfo='none'
        ))
        fig_bar.update_layout(
            title=f'{category} - Budget vs. Spent',
            yaxis=dict(range=[0, budget]),
            showlegend=False
        )

        # Display the title and the graphs
        with col0[0]:
            st.plotly_chart(fig_pie, use_container_width=True)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            
            
            
