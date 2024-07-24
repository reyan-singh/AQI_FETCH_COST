import requests
import geopy
import os
import json

# Define AQI category labels
aqi_labels = {
    0: 'good',
    1: 'moderate',
    2: 'unhealthy_sensitive',
    3: 'unhealthy',
    4: 'very_unhealthy',
    5: 'hazardous'
}

def get_lanlat():
    lan = input("Enter Langitude: ")
    lat = input("Enter Latitude: ")
    return lan, lat

# Function to get latitude and longitude from location name
def get_coordinates(location):
    geolocator = geopy.geocoders.Nominatim(user_agent="air_quality_app")
    location = geolocator.geocode(location)
    if location is None:
        raise ValueError("Location not found")
    return location.latitude, location.longitude

# Function to get AQI value from OpenWeatherMap API
def get_aqi(latitude, longitude):
    api_key = "c240a459dab670c0510091263e5a81ca"
    if not api_key:
        raise ValueError("API key not found. Set the OPENWEATHER_API_KEY environment variable.")
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if 'list' in data and len(data['list']) > 0:
        return json.dumps(data)
    else:
        raise ValueError("AQI data not found in API response")

# Function to determine air quality category
def get_aqi_category(aqi_value):
    return aqi_labels.get(aqi_value, 'unknown')

if __name__ == "__main__":


    location = input("Enter location: ")
    try:
        latitude, longitude =0,0
        if location=="":
            latitude, longitude = get_lanlat()
        else:
            latitude, longitude = get_coordinates(location)
        aqi_value =  get_aqi(latitude, longitude)

        data = aqi_value.replace("'", '"')

        adata = json.loads(data)

        lon = adata['coord']['lon']
        lat = adata['coord']['lat']
        aqi = adata['list'][0]['main']['aqi']
        co = adata['list'][0]['components']['co']
        no = adata['list'][0]['components']['no']
        no2 = adata['list'][0]['components']['no2']
        o3 = adata['list'][0]['components']['o3']
        so2 = adata['list'][0]['components']['so2']
        pm2_5 = adata['list'][0]['components']['pm2_5']
        pm10 = adata['list'][0]['components']['pm10']
        nh3 = adata['list'][0]['components']['nh3']
        dt = adata['list'][0]['dt']
        print(lon,aqi,so2,lon,pm10,nh3)
    except Exception as e:
        print("Error:", e)
