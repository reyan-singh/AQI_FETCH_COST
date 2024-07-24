import requests
import geopy
import os

# Define AQI category labels
aqi_labels = {
    0: 'good',
    1: 'moderate',
    2: 'unhealthy_sensitive',
    3: 'unhealthy',
    4: 'very_unhealthy',
    5: 'hazardous'
}

# Function to get latitude and longitude from location name
def get_coordinates(location):
    geolocator = geopy.geocoders.Nominatim(user_agent="air_quality_app")
    location = geolocator.geocode(location)
    if location is None:
        raise ValueError("Location not found")
    return location.latitude, location.longitude

# Function to get AQI value from OpenWeatherMap API
def get_aqi(latitude, longitude):
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Set the OPENWEATHER_API_KEY environment variable.")
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    # Debug: print the API response
    print("API Response:", data)

    if 'list' in data and len(data['list']) > 0:
        aqi_value = data['list'][0]['main']['aqi']
        return aqi_value
    else:
        raise ValueError("AQI data not found in API response")

# Function to determine air quality category
def get_aqi_category(aqi_value):
    return aqi_labels.get(aqi_value, 'unknown')

if __name__ == "__main__":
    location = input("Enter location: ")
    try:
        latitude, longitude = get_coordinates(location)
        aqi_value = get_aqi(latitude, longitude)
        aqi_category = get_aqi_category(aqi_value)
        print(f"{location} air quality is currently '{aqi_category}'")
    except Exception as e:
        print("Error:", e)
