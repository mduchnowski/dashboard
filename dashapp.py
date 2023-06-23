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
    st.write(str(days_until_payday(datetime.today().date())))