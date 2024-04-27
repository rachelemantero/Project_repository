import streamlit as st
import requests

def get_airport_suggestions(city):
    url = "https://sky-scanner3.p.rapidapi.com/flights/auto-complete"
    querystring = {"query": city, "placeTypes": "AIRPORT", "outboundDate": "2024-04-25"}
    headers = {
        "X-RapidAPI-Key": "36f23cc19bmsh7d1efbfa0a7d699p1f1977jsn5cd6d29c643a",
        "X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def extract_airport_info(response_data):
    airport_info = []
    for item in response_data['data']:
        suggestion_title = item['presentation']['suggestionTitle']
        sky_id = item['navigation']['relevantFlightParams']['skyId']
        presentation_id = item['presentation']['id']
        airport_info.append({'suggestionTitle': suggestion_title, 'skyId': sky_id, 'presentationId': presentation_id})
    return airport_info

def store_airport_ids(airports):
    airport_ids = {}
    for airport in airports:
        airport_ids[airport['skyId']] = airport['presentationId']
    return airport_ids

# User inputs
departure_city = input("Enter departure city: ")
arrival_city = input("Enter arrival city: ")

# Fetching data for both cities
departure_data = get_airport_suggestions(departure_city)
arrival_data = get_airport_suggestions(arrival_city)

# Extracting information
departure_airports = extract_airport_info(departure_data)
arrival_airports = extract_airport_info(arrival_data)

# Storing IDs
departure_airport_ids = store_airport_ids(departure_airports)
arrival_airport_ids = store_airport_ids(arrival_airports)

print("Departure Airport Suggestions:")
for airport in departure_airports:
    print(f"{airport['suggestionTitle']} - {airport['skyId']} (Presentation ID: {airport['presentationId']})")

print("Arrival Airport Suggestions:")
for airport in arrival_airports:
    print(f"{airport['suggestionTitle']} - {airport['skyId']} (Presentation ID: {airport['presentationId']})")

# Display stored IDs (optional)
print("Stored Departure Airport IDs:", departure_airport_ids)
print("Stored Arrival Airport IDs:", arrival_airport_ids)

#GIVES AIRPORTS AVAILABLE IN DEPARTURE AND ARRIVAL CITY AND THE ID VALUE NEEDED TO MAKE THE API REQUEST



def get_flight_search_results(from_entity_id, to_entity_id, depart_date, adults, children, infants, cabin_class):
    url = "https://sky-scanner3.p.rapidapi.com/flights/search-one-way"
    querystring = {
        "fromEntityId": from_entity_id,
        "toEntityId": to_entity_id,
        "departDate": depart_date,
        "adults": adults,
        "children": children,
        "infants": infants,
        "cabinClass": cabin_class
    }
    headers = {
        "X-RapidAPI-Key": "36f23cc19bmsh7d1efbfa0a7d699p1f1977jsn5cd6d29c643a",
        "X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def map_skyid_to_presentationid(airports):
    return {airport['skyId']: airport['presentationId'] for airport in airports}


# Map SkyIDs to PresentationIDs
departure_id_map = map_skyid_to_presentationid(departure_airports)
arrival_id_map = map_skyid_to_presentationid(arrival_airports)

# Get user input
skyid_departure = input("Enter your selected departure airport SKYID: ")
skyid_arrival = input("Enter your selected arrival airport SKYID: ")
depart_date = input("Enter the departure date (YYYY-MM-DD): ")
adults = input("Enter the number of adults (age 12+): ")
children = input("Enter the number of children (age 2-12): ")
infants = input("Enter the number of infants (age below 2): ")
cabin_class = input("Enter the cabin class (economy, premium_economy, business, first): ")

# Translate SKYIDs to PresentationIDs
from_entity_id = departure_id_map.get(skyid_departure, "Invalid SKYID")
to_entity_id = arrival_id_map.get(skyid_arrival, "Invalid SKYID")

# Fetching flight search results
flight_search_results = get_flight_search_results(
    from_entity_id,
    to_entity_id,
    depart_date,
    adults,
    children,
    infants,
    cabin_class
)

# Display the search results
print(flight_search_results)

#TAKES VARIOUS INPUT FROM THE USER AND DISPLAYS THE WHOLE RESULTS OF FLIGHT DATA OPTIONS FOUND


def extract_flight_details(flight_search_results):
    flights = flight_search_results['data']['itineraries']
    flight_details = []
    
    for flight in flights:
        details = {
            'priceFormatted': flight['price']['formatted'],
            'durationInMinutes': flight['legs'][0]['durationInMinutes'],
            'stopCount': flight['legs'][0]['stopCount'],
            'departure': flight['legs'][0]['departure'],
            'arrival': flight['legs'][0]['arrival'],
            'carriersName': [carrier['name'] for carrier in flight['legs'][0]['carriers']['marketing']],
            'carriersLogo': [carrier['logoUrl'] for carrier in flight['legs'][0]['carriers']['marketing']],  
            'flightNumber': flight['legs'][0]['segments'][0]['flightNumber'],
            'isCancellationAllowed': flight['farePolicy']['isCancellationAllowed'],
            'isPartiallyRefundable': flight['farePolicy']['isPartiallyRefundable']
        }
        flight_details.append(details)
    
    return flight_details


# Example usage:
flight_data = extract_flight_details(flight_search_results)
for flight in flight_data:
        print(flight)

#EXTRACT ONLY THE MOST USFEFUL FLIGHT DATA FROM THE OPTIONS


def sort_flights(flight_details, sort_by, ascending=True):
    if sort_by == 'priceFormatted':
        key_func = lambda x: float(x['priceFormatted'].strip('$').replace(',', ''))
    elif sort_by == 'durationInMinutes':
        key_func = lambda x: x['durationInMinutes']
    elif sort_by == 'carriersName':
        key_func = lambda x: x['carriersName'][0]  # Assumes there's at least one carrier name
    else:
        return flight_details  # No sorting if sort_by criteria is unknown
    
    return sorted(flight_details, key=key_func, reverse=not ascending)


# Sorting examples:
sorted_by_price_asc = sort_flights(flight_data, 'priceFormatted', True)
sorted_by_price_desc = sort_flights(flight_data, 'priceFormatted', False)
sorted_by_duration_asc = sort_flights(flight_data, 'durationInMinutes', True)
sorted_by_duration_desc = sort_flights(flight_data, 'durationInMinutes', False)
sorted_by_carrier_name = sort_flights(flight_data, 'carriersName', True)

# Printing sorted results:
print("Sorted by Price Ascending:")
for flight in sorted_by_price_asc:
    print(flight)
print("Sorted by Carrier Name Alphabetically:")
for flight in sorted_by_carrier_name:
    print(flight)

#ALLOWS TO SORT THE DATA OF THE FLIGH OPTIONS BY PRICE, DURATION and CARRIER NAME