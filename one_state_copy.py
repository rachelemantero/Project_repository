import streamlit as st
import requests
from DataBase_Countries import get_country_code, get_country_name

def run_visa_country_status(passport_country):
    passport_code = get_country_code(passport_country)
    if not passport_code:
        st.error(f"'{passport_country}' is not recognized. Please enter a valid country name.")
        return None, None, None, None, None  # Return None for all categories if the country code is not found

    url = f'https://rough-sun-2523.fly.dev/api/{passport_code}'
    response = requests.get(url)
    data = response.json()

    if data:
        visa_required = [get_country_name(code) for code in data.get('vr', {}).get('data', [])]
        visa_on_arrival = [get_country_name(code) for code in data.get('voa', {}).get('data', [])]
        visa_free = [get_country_name(code) for code in data.get('vf', {}).get('data', [])]
        covid_ban = [get_country_name(code) for code in data.get('cb', {}).get('data', [])]
        no_admission = [get_country_name(code) for code in data.get('na', {}).get('data', [])]
        return visa_required, visa_on_arrival, visa_free, covid_ban, no_admission

    return None, None, None, None, None  # Return None for all lists if there is no data

# Streamlit interface to input country and get visa status
def visa_status_interface():
    st.title('Visa Country Status')
    passport_country = st.text_input("Enter your passport country:", key='passport_country')

    if st.button('Get Visa Status') and passport_country:
        required, on_arrival, free, covid_banned, no_admit = run_visa_country_status(passport_country)
        if required is not None:
            st.write("Visa Required Countries:", ', '.join(required))
            st.write("Visa on Arrival Countries:", ', '.join(on_arrival))
            st.write("Visa Free Countries:", ', '.join(free))
            st.write("Covid Ban Countries:", ', '.join(covid_banned))
            st.write("No Admission Countries:", ', '.join(no_admit))
        else:
            st.write("No visa information available for this country.")

visa_status_interface()
