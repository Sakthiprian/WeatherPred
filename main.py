import requests
import pandas as pd
import time
from datetime import datetime
from dataduino import duino
import os

api_url = 'https://api.weatherbit.io/v2.0/current'

params = {
    'lat': '12.8513',   # latitude of kandigai
    'lon': '80.1470',   # longitude of kandigai
    'key': '947141b2db6e415bb279750e5775f1ae',  # Weatherbit API key
    'units': 'M',  # Metric units (you can change this to 'I' for imperial or 'S' for scientific)
}

headers = {
    'Cache-Control': 'no-cache'
}

df = pd.DataFrame()  # Create an empty DataFrame outside the loop
ser = duino.duinodata('COM11')
time.sleep(7)

while True:
    try:
        response = requests.get(api_url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            for item in data['data']:
                attr = ser.read()
                data_model = {
                    'temperature': attr['temperature'],
                    'humidity': attr['humidity'],
                    'light': attr['light'],
                    'weather_description': item['weather']['description'],
                    'time_obs': item['ob_time'],
                    'time_rec':datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                temp_label = pd.DataFrame([data_model])  # Create a DataFrame for each data point
                df = pd.concat([df, temp_label])  # Append the data to the main DataFrame
                print(df)

                # Append the newest row to the CSV file
                temp_label.to_csv('weather_data.csv', mode='a', header=False, index=False)
                
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

        response.close()

    except requests.RequestException as e:
        print(f"Error: {e}")
        # Sleep for a while before trying again
        time.sleep(60)  # Sleep for 1 minutes in case of network issues

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    time.sleep(600)  # Sleep for 2 minutes between each iteration
    os.system('cls' if os.name == 'nt' else 'clear')
