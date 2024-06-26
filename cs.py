#cs.py
# This file creates a navigation bar with all the three features

import streamlit as st
from two_states import run_visa_checker
from one_state import run_visa_country_status
from Flight_data import flight_main

st.set_page_config(page_title="Check-It")

# Function that pulls together all the features
def main():

    # Large sidebar title using HTML for serif font styling
    st.sidebar.markdown(
        "<h1 style='font-size: 32px; color: black; margin-top: 0; font-family: \"Times New Roman\", Times, serif;'>Check-It ✅</h1>", 
        unsafe_allow_html=True
    )

    # Adding custom spacing using HTML & inline CSS
    st.sidebar.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Sidebar navigation and welcome text
    st.sidebar.write("Welcome to your Visa and Travel Assistant! Select a feature from the list below to get started.")
    app_option = st.sidebar.selectbox('Choose a feature:',
                                      ['Two States', 'One State', 'Flight Search'])

    # Conditional execution based on sidebar selection
    if app_option == 'Two States':
        run_visa_checker()
    elif app_option == 'One State':
        run_visa_country_status()
    elif app_option == 'Flight Search':
        flight_main ()

if __name__ == "__main__":
    main()
