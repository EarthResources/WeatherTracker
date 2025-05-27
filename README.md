# WeatherTracker
This script uses the weather restrictions for bat acoutsic surveys per the USFWS Florida Bonneted Bat survey protocol and sends an email notification with the metric ranges and a `PASS` or `FAIL` status. For more information on the USFWS protocol, see [here](https://www.fws.gov/sites/default/files/documents/2024-07/20240605_final_fbb-consultation-guidance_0.pdf). This script uses the National Weather Service [API](https://www.weather.gov/documentation/services-web-api) and reads it into a `pandas` dataframe. That information is summed up as a range of min and max values and sent to the user using the `smtplib` library. See example provided in this repo.

## Requirements
+ Gmail account with 2FA enabled
+ Gmail app password

## Example email format

From: {sender}<br>
To: {receiver}<br>
Subject: Bat Survey Weather Alert 2025-05-27 - PASS<br>


Below are the weather metrics:<br>
Temp (F): 65-73 <br>
Wind (mph): 2-6 <br>
Precip (mm): 0 <br>