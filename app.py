import requests
import streamlit as gr

# Function to fetch weather data
def get_weather(city):
    # Use Open-Meteo's geocoding API to get coordinates of the city
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_response = requests.get(geo_url).json()

    if "results" not in geo_response:
        return f"❌ City '{city}' not found. Try again."

    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]

    # Fetch weather forecast from Open-Meteo API
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_response = requests.get(weather_url).json()

    if "current_weather" not in weather_response:
        return "❌ Could not fetch weather data."

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

    return f"📍 City: {city}\n🌡️ Temperature: {temperature} °C\n💨 Windspeed: {windspeed} km/h\n🌤️ Condition: {condition_text}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align:center'>🌦️ Weather Forecast App by ABM</h1>")
    city = gr.Textbox(label="Enter City Name")
    output = gr.Textbox(label="Weather Report")
    btn = gr.Button("Get Forecast")
    btn.click(get_weather, inputs=city, outputs=output)

# Run the app
if __name__ == "__main__":
    demo.launch()
