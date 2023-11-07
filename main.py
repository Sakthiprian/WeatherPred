import requests
import pandas as pd
import time
from datetime import datetime

api_url = 'https://api.weatherbit.io/v2.0/current'

params = {
    'lat': '13.124620',   # latitude of Kandigai
    'lon': '80.193176',   # longitude of Kandigai
    'key': 'd8444b8f69634c0b9d3369b034820820',  # Weatherbit API key
    'units': 'M',  # Metric units (you can change this to 'I' for imperial or 'S' for scientific)
}

headers = {
    'Cache-Control': 'no-cache'
}

df = pd.DataFrame()  # Create an empty DataFrame outside the loop

while True:

    response = requests.get(api_url, params=params,headers=headers)

    if response.status_code == 200:
        data = response.json()
        for item in data['data']:
            data_model = {
                'temp': item['temp'],
                'pres': item['pres'],
                'relative humidity': item['rh'],
                'last_obs': item['ob_time'],
                'time_now':datetime.now().strftime("%H:%M:%S"),
                'weather_description': item['weather']['description']
            }
            temp = pd.DataFrame([data_model])  # Create a DataFrame for each data point
            df = pd.concat([df, temp])  # Append the data to the main DataFrame
            print(df)
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

    response.close()

    time.sleep(600)
