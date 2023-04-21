import streamlit as st
import requests
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

st.set_page_config(layout="wide")

st.title("Real Estate Investment Analysis Tool")

limit = 100
response = requests.get(f"http://localhost:5000/properties?limit={limit}")

print("Status code:", response.status_code)
print("Response content:", response.content)
data = response.json()

st.write("Properties Data")

# Flatten the nested JSON structure and create separate columns for each nested key
df = json_normalize(data)

def is_good_deal(row):
    return row['price.price'] < row['price.zestimate']*1.1

df['good_deal'] = df.apply(is_good_deal, axis=1)
good_deals = df[df['good_deal']]

st.write("Good Deals")
st.write(good_deals)

def extract_lat_lng(address):
    try:
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=AIzaSyD4EZjIMyqry2VYI9RimEwsr6a3c3xPKB4"
        response = requests.get(geocode_url)
        location_data = response.json()
        lat_lng = location_data['results'][0]['geometry']['location']
        return lat_lng['lat'], lat_lng['lng']
    except Exception as e:
        print(f"Error extracting lat/lng for address {address}: {e}")
        return np.nan, np.nan

# Extract latitudes and longitudes
lat_lng_df = good_deals['address.address'].apply(extract_lat_lng).apply(pd.Series)
lat_lng_df.columns = ['lat', 'lon']
# Remove rows with NaN values
lat_lng_df = lat_lng_df.dropna(subset=['lat', 'lon'])

# Assign latitudes and longitudes to the good_deals DataFrame
good_deals = good_deals.loc[lat_lng_df.index]
good_deals[['lat', 'lon']] = lat_lng_df

# Create a map of good deals using Streamlit's built-in map function
st.map(good_deals)
