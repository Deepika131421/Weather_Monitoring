import requests
from datetime import datetime
import time
import csv

API_KEY = '1ce46afbe4fd66435f9f156b81f5ca53'
CITY = 'Delhi'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

# To store daily weather records
weather_records = []

# User-configurable thresholds
TEMP_THRESHOLD = 35  # Set your temperature threshold (in Celsius)

def get_weather_data(city):
    try:
        url = BASE_URL.format(city, API_KEY)
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extracting relevant data
        temp_kelvin = data['main']['temp']
        weather_condition = data['weather'][0]['main']  # Main weather condition
        timestamp = data['dt']  # Unix timestamp
        
        # Convert temperature from Kelvin to Celsius
        temp_celsius = temp_kelvin - 273.15
        
        # Append to records
        weather_records.append({
            'temperature': temp_celsius,
            'condition': weather_condition,
            'timestamp': timestamp
        })

        print(f"Weather data for {city}:")
        print(f"Current Temperature: {temp_celsius:.2f} °C")
        print(f"Weather Condition: {weather_condition}")
        print(f"Data Updated At: {datetime.fromtimestamp(timestamp)}")
        
        # Check for alerts
        if temp_celsius > TEMP_THRESHOLD:
            print(f"ALERT: Temperature exceeds threshold! Current Temperature: {temp_celsius:.2f} °C")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error: Unable to connect to the OpenWeatherMap API. {conn_err}")
    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
    except Exception as err:
        print(f"An error occurred: {err}")

def calculate_daily_summary():
    if not weather_records:
        print("No weather records to summarize.")
        return
    
    total_temp = 0
    max_temp = float('-inf')
    min_temp = float('inf')
    condition_counts = {}

    # Process records for today
    for record in weather_records:
        total_temp += record['temperature']
        max_temp = max(max_temp, record['temperature'])
        min_temp = min(min_temp, record['temperature'])

        # Count weather conditions
        condition = record['condition']
        condition_counts[condition] = condition_counts.get(condition, 0) + 1

    avg_temp = total_temp / len(weather_records)
    dominant_condition = max(condition_counts, key=condition_counts.get)

    # Display daily summary
    print("\nDaily Weather Summary:")
    print(f"Average Temperature: {avg_temp:.2f} °C")
    print(f"Maximum Temperature: {max_temp:.2f} °C")
    print(f"Minimum Temperature: {min_temp:.2f} °C")
    print(f"Dominant Weather Condition: {dominant_condition}")

    # Save the records to a CSV file
    save_to_csv()

def save_to_csv(filename='weather_data.csv'):
    # Define the headers
    headers = ['timestamp', 'temperature', 'condition']

    # Open the CSV file for writing
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write the headers

        # Write each weather record
        for record in weather_records:
            writer.writerow([datetime.fromtimestamp(record['timestamp']), record['temperature'], record['condition']])

    print(f"Weather records saved to {filename}.")

# Main loop to fetch data every 5 minutes (for demonstration, will run 3 times)
for _ in range(3):  # Run 3 times, can change as needed
    get_weather_data(CITY)
    time.sleep(300)  # Wait for 5 minutes

# Calculate and display the daily summary after fetching data
calculate_daily_summary()
