# WeatherTracker
This script uses the weather restrictions for bat acoutsic surveys per the USFWS Indiana Bat survey protocol and sends an email notification with the metric ranges and a `PASS` or `FAIL` status. For more information on the USFWS protocol, see [here](https://www.fws.gov/library/collections/range-wide-indiana-bat-and-northern-long-eared-bat-survey-guidelines).

## Requirements
+ Gmail account with 2FA enabled
+ Gmail app password

## Example email format

From: sender<br>
To: receiver<br>
Subject: Bat Survey Weather Alert - {PASS | FAIL}<br>


Below are the weather metrics:<br>
Temp (F): 65-73 <br>
Wind (mph): 2-6 <br>
Precip (in): 0 <br>


