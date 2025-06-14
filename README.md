# WeatherTracker
This script uses the weather restrictions for bat acoutsic surveys per the USFWS Florida Bonneted Bat survey protocol and sends an email notification with the metric ranges and a `PASS` or `FAIL` status. For more information on the USFWS protocol, see [here](https://www.fws.gov/sites/default/files/documents/2024-07/20240605_final_fbb-consultation-guidance_0.pdf). This script uses the National Weather Service [API](https://www.weather.gov/documentation/services-web-api) and reads it into a `pandas` dataframe. That information is summed up as a range of min and max values and sent to the user using the `smtplib` library. See example provided in this repo.

## Requirements
+ Gmail account with 2FA enabled
+ Gmail app password (or other client equivalent)
+ GitHub account

## Example email format

From: {sender}<br>
To: {receiver}<br>
Subject: Bat Survey Weather Alert YYYY-MM-DD - PASS<br>

Below are the weather metrics:<br>
Temp (F): 65-73 <br>
Wind (mph): 2-6 <br>
Precip (mm): 0 <br>

## How To Use

### Option 1: Running Locally
To use locally, clone the repository on your machine. 

```bash
git clone https://github.com/bofethe/WeatherTracker.git
```

Navigate to the [.env.example](.env.example) file and add your credentials for your app password and sender address.  Rename this file to `.env`.  Create a python 3.11 environment using something like venv or conda and install the libraries listed in the [requirements.txt](requirements.txt) file 


Using conda (needs installing)
```bash
conda create --name WeatherTracker --file requirements.txt
conda activate WeatherTracker
```

Using venv (built-in) to install

+ MacOS/Linux
```bash
python3.11 -m venv WeatherTracker
source WeatherTracker/bin/activate
pip install -r requirements.txt
```

+ Windows Command Prompt
```cmd
python3.11 -m venv WeatherTracker
WeatherTracker\Scripts\activate
pip install -r requirements.txt
```

Now run the [WeatherTracker.py](WeatherTracker.py) file


### Option 2: Scheduling on GitHub

To use this tool, fork the repository so you can host it in your own GitHub Account or organization.  In the repository's main menu, near the top right of the toolbar, drop down fork and select Create A New Fork. Add whatever details you want.

The script is preconfigured for scheduling using a CI pipeline that GitHub provides called GitHub Actions. Navigate to [weather.yml](.github/workflows/weather.yml) file and adjust the cron variable to the time you want to run.  Note that the timezone defaults to UTC, so adjust accordingly.

To handle authentication, you must add a secret to avoid hard-coding credentials. Open the repository's Settings page. Under Security, open Actions.  Create a repository secrets called `APPPW` for your email app password, and another called `SENDERADDR` for your email address. 

Once you're done, commit your changes. Then navigate to the Actions tab. Near the top right, select Enable Workflow. 

Once you're done collecting data, navigate back to the Actions tab, select Run WeatherTracker, and in teh top right next to where it says Filter workflow runs, click the `...` and select Disable Workflow.