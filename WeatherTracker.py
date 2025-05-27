import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz
from astral import LocationInfo
from astral.sun import sun
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Setup
stations = {'Tallahassee Airport': 'KTLH',
            'Ft Myers Page Field': 'KFMY'}

url = f"https://api.weather.gov/stations/{stations['Ft Myers Page Field']}/observations"
headers = {"User-Agent": "weather-observer"}

# Fetch observations
response = requests.get(url, headers=headers)
data = response.json()
observations = data.get("features", [])

# Parse records
long, lat = observations[0]['geometry']['coordinates']
records = []
for obs in observations:
    props = obs["properties"]
    record = {
        'station_name': props.get('stationName'),
        "station_id": props.get("stationId"),
        "timestamp_utc": pd.to_datetime(props.get("timestamp")),
        "temperature_c": props.get("temperature", {}).get("value"),
        "wind_speed_kph": props.get("windSpeed", {}).get("value"),
        "precip_mm": props.get("precipitationLastHour", {}).get("value"),
        'description': props.get("textDescription"),
        'source': props.get("@id")
    }
    records.append(record)

df = pd.DataFrame(records)

# Convert to local time (Eastern Time)
eastern = pytz.timezone("US/Eastern")
df["timestamp_local"] = df["timestamp_utc"].dt.tz_convert(eastern)

# Convert wind speed from kph to mph
df["wind_speed_mph"] = df["wind_speed_kph"] * 0.621371

# Convert temperature from Celsius to Fahrenheit
df["temperature_f"] = df["temperature_c"] * 9/5 + 32

# Get sunset time using astral
city = LocationInfo(latitude=lat, longitude=long)
now_local = datetime.now(eastern)
yesterday = now_local - timedelta(days=1)
sun_times = sun(city.observer, date=yesterday.date(), tzinfo=eastern)

start_time = sun_times["sunset"]
end_time = start_time + timedelta(hours=5)

# Filter for 5 hours after sunset
mask = (df["timestamp_local"] >= start_time) & (df["timestamp_local"] <= end_time)
evening_df = df.loc[mask]

# log the weather data
log_file = 'weatherLogs.csv'
if not os.path.exists(log_file):
    evening_df.to_csv(log_file, index=False)
else:
    evening_df.to_csv(log_file, mode='a', header=False, index=False)

# Compile weather ranges
airmin = evening_df['temperature_f'].min()
airmax = evening_df['temperature_f'].max()
windmin = evening_df['wind_speed_mph'].min()
windmax = evening_df['wind_speed_mph'].max()
precipsum = evening_df['precip_mm'].sum()

# Determine if it's a pass or fail based on USFWS standards
if airmin < 60 or windmax > 9 or precipsum > 0:
    status = 'FAIL'
else:
    status = 'PASS'

# Setup email
load_dotenv()
senderaddr = os.getenv('senderaddr')
apppw = os.getenv('apppw')
receiveraddr = 'bfethe@earthresources.us' #NOTE Update to whatever emails you want to send to

message = MIMEMultipart()
message['From'] = senderaddr
message['To'] = receiveraddr
message['Subject'] = f'Bat Survey Weather Alert {now_local.strftime("%Y-%m-%d")} - {status}'

body = f'''Below are the weather metrics:
Temp (F):       {airmin} - {airmax}
Wind (mph):     {windmin} - {windmax}
Precip (mm):    {precipsum}
'''
message.attach(MIMEText(body, 'plain'))

# Send the email
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as session:
        session.starttls()
        session.login(user=senderaddr, password=apppw)
        session.send_message(message)
    print('Email sent!')
except Exception as e:
    print(f"Failed to send email: {e}")
