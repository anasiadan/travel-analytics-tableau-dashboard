import pandas as pd
import numpy as np

# Mapping dictionaries for data cleaning and categorizing
country_mapping = {
        'AUS': 'Australia', 'Aus': 'Australia', 'AU': 'Australia',
        'Thai': 'Thailand', 'TH': 'Thailand',
        'SA': 'South Africa', 'RSA': 'South Africa',
        'UK': 'United Kingdom', 'GB': 'United Kingdom',
        'USA': 'United States', 'US': 'United States',
        'UAE': 'United Arab Emirates',
    }

city_to_country_mapping = {
        'Paris': 'France', 'Rome': 'Italy', 'London': 'United Kingdom',
        'Tokyo': 'Japan', 'Seoul': 'South Korea', 'Beijing': 'China',
        'Bangkok': 'Thailand', 'Phuket': 'Thailand', 'Singapore': 'Singapore', 'Mumbai': 'India',
        'Dubai': 'United Arab Emirates', 'Sydney': 'Australia',
        'Cape Town': 'South Africa', 'Cairo': 'Egypt', 'Phnom Penh': 'Cambodia', 'Santorini': 'Greece',
        'New York': 'United States', 'Toronto': 'Canada', 'Barcelona': 'Spain',
        'Mexico City': 'Mexico', 'Rio de Janeiro': 'Brazil', 'Bali': 'Indonesia', 'Amsterdam': 'Netherlands', 'Honolulu': 'Hawaii'
    }
transport_mapping = {
        'Flight': 'Air', 'Plane': 'Air', 'Airplane': 'Air',
        'Train': 'Rail', 'Subway': 'Rail',
        'Bus': 'Ground', 'Car': 'Ground', 'Car rental': 'Ground'
    }
season_mapping = {
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Fall', 10: 'Fall', 11: 'Fall'
    }
nationality_mapping = {
    'Brazil': 'Brazilian', 'United States': 'American', 'United Kingdom': 'British', 'USA': 'American',
    'Australia': 'Australian', 'Canada': 'Canadian', 'Germany': 'German', 'United Arab Emirates': 'Emirati',
    'France': 'French', 'Italy': 'Italian', 'Japan': 'Japanese', 'UK': 'British', 'Singapore': 'Singaporian',
    'South Korea': 'Korean', 'China': 'Chinese', 'India': 'Indian', 'Greece': 'Greek', 'Hong Kong': 'Chinese',
    'Spain': 'Spanish', 'Netherlands': 'Dutch', 'Thailand': 'Thai', 'Taiwan': 'Taiwanese', 'Cambodia': 'Cambodian'
}

# Convert mapping dictionaries to lists for comparison operations
cities_list = list(city_to_country_mapping.keys())
country_list = list(city_to_country_mapping.values())
country_abbreviations = list(country_mapping.keys())


def clean_data(df):
    # Remove null values and create working copy
    df = df.dropna().copy()

    # Create boolean masks to identify destination formats
    destination_has_city_and_country = df['Destination'].str.contains(',')
    is_destination_a_city = df['Destination'].isin(cities_list)
    is_destination_a_country = df['Destination'].isin(country_list)
    
    # Using different methods to extract data to be used in new columns
    df['Temp_col_1'] = df['Destination'].map(city_to_country_mapping)
    df['Temp_col_2'] = df['Destination'].str.extract(r',\s*([^,]+)$')[0]
    df['Temp_col_3'] = df['Temp_col_2'].map(country_mapping)
    df['Temp_col_4'] = df['Destination'].str.extract(r'^([^,]+)')[0]
    df['Temp_col_5'] = df['Traveler nationality'].map(nationality_mapping)

    # Transform the cost columns in float type and remove the USD,$ symbols
    df['Accommodation cost'] = df['Accommodation cost'].str.translate(str.maketrans('','',',$USD')).astype(float)
    df['Transportation cost'] = df['Transportation cost'].str.translate(str.maketrans('','',',$USD')).astype(float)

    # Transfrom the date columns to datetime type
    df['Start date'] = pd.to_datetime(df['Start date'])
    df['End date'] = pd.to_datetime(df['End date'])

    # Create new columns for Country and City instead of Destination
    df['Country'] = np.where(destination_has_city_and_country,df['Temp_col_2'],np.where(is_destination_a_city,df['Temp_col_1'],np.where(is_destination_a_country,df['Destination'],'Unknown')))
    df['City'] = np.where(destination_has_city_and_country,df['Temp_col_4'],np.where(is_destination_a_city,df['Destination'],'Unknown'))
    df['Traveler nationality'] = df['Traveler nationality'].map(nationality_mapping).fillna(df['Traveler nationality'])

    # Create more column metrics and categories
    df['Transport_Category'] = df['Transportation type'].map(transport_mapping)
    df['Total_Cost'] = df['Accommodation cost'] + df['Transportation cost']
    df['Cost_Per_Day'] = round(df['Total_Cost'] / df['Duration (days)'],2)
    df['Travel_Month'] = pd.to_datetime(df['Start date']).dt.month_name()
    df['Travel_Season'] = pd.to_datetime(df['Start date']).dt.month.map(season_mapping)

    # Replace country abbreviations with full country names
    df['Country'] = np.where(df['Country'].isin(country_abbreviations),df['Temp_col_3'],df['Country'])


    # Clean up temporary columns and Destination column which is replaced from City and Country columns
    df = df.drop(columns =['Temp_col_1', 'Temp_col_2', 'Temp_col_3', 'Temp_col_4', 'Temp_col_5', 'Destination'])

    return df
    
