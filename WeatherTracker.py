import requests
import pandas as pd
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

'''
This script takes the data from a NOAA weather station and sends an email with a summary of the first 5 hours
per the USFWS protocol for bat acoustic surveys.
'''

# Define start and end time to track the weather
start = '18:00'
end = '23:00'

# Get the weather page html
stationURL = 'https://w1.weather.gov/data/obhistory/KTLH.html'
page = requests.get(stationURL)

# Get the dataframes and drop last 3 rows due to malformatting
df_all = pd.read_html(page.text)
df_weather = df_all[3].iloc[:-3]

# Flatten multilevel columns
df_weather.columns = df_weather.columns.droplevel([0,1])

# Filter to the first 5 hours after sunset per USFWS protocol for the night
df_weather_select = df_weather[(df_weather['Time(est)'] > start) & 
                                (df_weather['Time(est)'] < end) & 
                                (df_weather['Date'] == df_weather['Date'].max())].copy()


# Clean up the wind and precipitation to just numeric
df_weather_select['Wind'] = df_weather_select['Wind(mph)'].str.extract(r'(\d+)').fillna(0)
df_weather_select['1 hr'] = df_weather_select['1 hr'].fillna(0)

# Set data types for remaining fields
ftypes = {'Date': int, 'Wind': int, 'Air': int}
df_weather_select = df_weather_select.astype(ftypes)

# Compile weather ranges
airmin = df_weather_select['Air'].min()
airmax = df_weather_select['Air'].max()
windmin = df_weather_select['Wind'].min()
windmax = df_weather_select['Wind'].max()
precipsum = df_weather_select['1 hr'].sum()

# Determine if its a pass or fail based on USFWS standards
if airmin < 50 or windmax > 9 or precipsum > 0:
    status = 'FAIL'
else:
    status = 'PASS'

# Setup email
senderaddr = os.getenv('senderaddr')
senderpw = os.getenv('senderpw')
receiveraddr = 'bfethe@hntb.com'

message = MIMEMultipart()
message['From'] = senderaddr
message['To'] = receiveraddr
message['Subject'] = f'Bat Survey Weather Alert - {status}'

body = f'''Below are the weather metrics:
Temp (F):       {airmin} - {airmax}
Wind (mph):     {windmin} - {windmax}
Precip (in):    {precipsum}
'''
message.attach(MIMEText(body, 'plain'))

# Send the email
session = smtplib.SMTP(host='smtp.gmail.com', port=587)
session.starttls()
session.login(user=senderaddr, password=senderpw)
text = message.as_string()
sendErr = session.sendmail(msg=text, from_addr=senderaddr, to_addrs=receiveraddr)
session.quit()

print('Done!')