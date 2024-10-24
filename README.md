Real_Time Weather Monitoring System with Rollups and Aggregates


Introduction 

This Python project implements a real-time weather monitoring system that continuously retrieves weather data from OpenWeatherMap for major Indian metros (Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad). It processes the data, calculates daily summaries with rollups and aggregates, provides alerting thresholds, and persists the summaries to a database or storage system.

System Overview :

The system comprises the following key components:
 * Data Acquisition:
   * Fetches real-time weather data from OpenWeatherMap at configurable intervals (e.g., every 5 minutes) using a valid API key.
   * Parses the JSON response to extract relevant fields:
     * main: Weather condition (e.g., Rain, Snow, Clear)
     * temp: Temperature (Kelvin)
     * feels_like: Perceived temperature (Kelvin)
     * dt: Time of data update (Unix timestamp)
 * Data Processing:
   * Converts temperature values from Kelvin to Celsius based on user preference (assumed to be Celsius).
 * Rollups and Aggregates:
   * Daily Weather Summary:
     * Rolls up weather data for each day.
     * Calculates daily aggregates for:
       * Average temperature
       * Maximum temperature
       * Minimum temperature
       * Dominant weather condition (determined by the most frequent occurrence)
     * Stores summaries in a database or persistent storage for further analysis.
   * Alerting Thresholds:
     * Defines user-configurable thresholds for temperature or specific weather conditions (implementation not provided in this version).
 * Data Persistence:
   * Stores calculated daily summaries in a database or storage system of your choice.

 Technologies Used :
 
  * Python: Core programming language for data fetching and processing.
  * SQLite: Database used for storing persistent weather data.
  * Pandas: Python library for handling CSV data.
  * Requests: Used to make API calls to OpenWeatherMap.
  * OpenWeatherMap API: Provides real-time weather data.

Conclusion :

This project helps monitor and persist real-time weather data from multiple cities in India. The data is stored in both a SQLite database for structured persistence and a CSV file for easy viewing and analysis.   
