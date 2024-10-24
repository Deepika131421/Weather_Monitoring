import requests
import json
from datetime import datetime
from collections import Counter
import sqlite3
import time

# Replace with your OpenWeatherMap API key
API_KEY = '1ce46afbe4fd66435f9f156b81f5ca53'
# City IDs for major Indian metros
CITY_IDS = {
    "Delhi": 1273294,
    "Mumbai": 1275339,
    "Chennai": 1264527,
    "Bangalore": 1277333,
    "Kolkata": 1275004,
    "Hyderabad": 1269843,
}

# Configurable polling interval (minutes)
POLLING_INTERVAL = 5

# Database connection logic
def connect_to_storage():
    connection = sqlite3.connect("weather_data.db")
    create_tables(connection)
    return connection

def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            date TEXT,
            avg_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_condition TEXT
        )
    """)
    connection.commit()

def store_daily_summary(data, connection):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO daily_summaries (city, date, avg_temp, max_temp, min_temp, dominant_condition)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data["city"], data["date"], data["avg_temp"], data["max_temp"], data["min_temp"], data["dominant_condition"]))
    connection.commit()
    print(f"Stored summary for {data['city']} on {data['date']}")  # Debugging message

def get_weather_data(city_id):
    url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Data fetched for city ID {city_id}")  # Debugging message
        return response.json()
    else:
        print(f"Error fetching data for city ID {city_id}: {response.status_code}")
        return None

def process_weather_data(data):
    if "weather" in data and "main" in data:
        weather_condition = data["weather"][0]["main"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        dt = datetime.fromtimestamp(data["dt"])

        return {
            "city": data["name"],
            "condition": weather_condition,
            "temp_celsius": temperature,
            "feels_like_celsius": feels_like,
            "dt": dt,
        }
    else:
        print("Unexpected data format:", data)  # Debugging message
        return None

def calculate_daily_summary(weather_data):
    daily_data = {}
    for data in weather_data:
        date = data["dt"].date()
        if date not in daily_data:
            daily_data[date] = {
                "temperatures": [],
                "conditions": Counter(),
                "city": data["city"],
            }
        daily_data[date]["temperatures"].append(data["temp_celsius"])
        daily_data[date]["conditions"][data["condition"]] += 1

    daily_summaries = []
    for date, data in daily_data.items():
        avg_temp = sum(data["temperatures"]) / len(data["temperatures"])
        max_temp = max(data["temperatures"])
        min_temp = min(data["temperatures"])
        dominant_condition = data["conditions"].most_common(1)[0][0]

        daily_summaries.append({
            "city": data["city"],
            "date": date,
            "avg_temp": avg_temp,
            "max_temp": max_temp,
            "min_temp": min_temp,
            "dominant_condition": dominant_condition,
        })

    return daily_summaries

def main():
    connection = connect_to_storage()
    while True:
        weather_data_list = []
        for city_name, city_id in CITY_IDS.items():
            weather_data = get_weather_data(city_id)
            if weather_data:
                processed_data = process_weather_data(weather_data)
                if processed_data:
                    print(f"Processed data for {city_name}: {processed_data}")  # Debugging message
                    weather_data_list.append(processed_data)
            else:
                print(f"Failed to fetch data for {city_name}")  # Debugging message
        if weather_data_list:
            daily_summaries = calculate_daily_summary(weather_data_list)
            for summary in daily_summaries:
                store_daily_summary(summary, connection)
        else:
            print("No weather data to process.")  # Debugging message
        time.sleep(POLLING_INTERVAL * 60)

if __name__ == "__main__":
    main()
