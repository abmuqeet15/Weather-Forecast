import requests
import streamlit as st

# Function to fetch weather data
def get_weather(city):
    # Use Open-Meteo's geocoding API to get coordinates of the city
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_response = requests.get(geo_url).json()

    if "results" not in geo_response:
        return None, f"❌ City '{city}' not found. Try again."

    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]

    # Fetch weather forecast from Open-Meteo API
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_response = requests.get(weather_url).json()

    if "current_weather" not in weather_response:
        return None, "❌ Could not fetch weather data."

    weather = weather_response["current_weather"]
    temperature = weather["temperature"]
    windspeed = weather["windspeed"]
    condition = weather["weathercode"]

    # Map weather codes to readable conditions
    weather_codes = {
        0: "Clear sky ☀️", 1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅", 3: "Overcast ☁️",
        45: "Fog 🌫️", 48: "Depositing rime fog 🌫️", 51: "Light drizzle 🌦️",
        61: "Rainy 🌧️", 71: "Snowfall ❄️", 95: "Thunderstorm ⛈️"
    }
    condition_text = weather_codes.get(condition, "Unknown")

    report = {
        "city": city,
        "temperature": f"{temperature} °C",
        "windspeed": f"{windspeed} km/h",
        "condition": condition_text
    }

    return report, None


# Streamlit App
st.set_page_config(page_title="Weather Forecast App", page_icon="🌦️", layout="centered")

st.title("🌦️ Weather Forecast App")
city = st.text_input("Enter City Name:")

if st.button("Get Forecast"):
    report, error = get_weather(city)
    if error:
        st.error(error)
    else:
        st.success(f"📍 City: {report['city']}")
        st.write(f"🌡️ Temperature: {report['temperature']}")
        st.write(f"💨 Windspeed: {report['windspeed']}")
        st.write(f"🌤️ Condition: {report['condition']}")
