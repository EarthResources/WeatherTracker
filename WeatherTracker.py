import requests
import pandas as pd

start = '18:00'
end = '23:00'

# Get the weather page html
stationURL = 'https://w1.weather.gov/data/obhistory/KTLH.html'
page = requests.get(stationURL)

# get the dataframes
df_all = pd.read_html(page.text)
df_weather = df_all[3]

# flatten multilevel columns
df_weather.columns = df_weather.columns.droplevel([0,1])

# filter to the first 5 hours of sunset per USFWS protocol
df_weather_select = df_weather[(df_weather['Time(est)'] > start) & (df_weather['Time(est)'] < end)]

# Compile weather range

# Determine if its a pass or fail based on USFWS standards

# Compile message

# Send message