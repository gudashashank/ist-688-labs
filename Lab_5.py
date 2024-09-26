import streamlit as st
import requests
from openai import OpenAI
import anthropic

# Set up Streamlit secrets for API keys
OPENWEATHER_API_KEY = st.secrets["open-weather"]
OPENAI_API_KEY = st.secrets["openai_key"]
CLAUDE_API_KEY = st.secrets["claude-key"]

# Set up Streamlit UI
st.title("Weather Chatbot")

# Sidebar for LLM selection
st.sidebar.header("Settings")
llm_vendor = st.sidebar.selectbox("Select LLM Vendor", ("OpenAI", "Claude"))

# Input for city
location = st.text_input("Enter a city to get the weather:", "Syracuse, NY")

# Function to retrieve weather data
def get_current_weather(location, API_key):
    if "," in location:
        location = location.split(",")[0].strip()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_key}"
    response = requests.get(url)
    data = response.json()

    # Extract temperatures and convert Kelvin to Celsius
    temp = data['main']['temp'] - 273.15
    feels_like = data['main']['feels_like'] - 273.15
    temp_min = data['main']['temp_min'] - 273.15
    temp_max = data['main']['temp_max'] - 273.15
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']

    return {
        "location": location,
        "temperature": round(temp, 2),
        "feels_like": round(feels_like, 2),
        "temp_min": round(temp_min, 2),
        "temp_max": round(temp_max, 2),
        "humidity": humidity,
        "description": description
    }

# Function to generate clothing suggestions and picnic advice using LLM
def generate_clothing_and_picnic_advice(weather_info, llm_vendor):
    prompt = (f"Based on: {weather_info['location']}, {weather_info['description']}, {weather_info['temperature']}°C, "
              f"feels like {weather_info['feels_like']}°C, humidity {weather_info['humidity']}%. "
              "Briefly suggest clothing and whether it's good for a picnic (50 words max).")

    if llm_vendor == "OpenAI":
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a concise weather advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=75
        )
        return response.choices[0].message.content.strip()

    elif llm_vendor == "Claude":
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=75,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text.strip()

# Main function for processing the weather data
def process_weather_request(location, llm_vendor):
    weather_info = get_current_weather(location, OPENWEATHER_API_KEY)
    clothing_suggestions = generate_clothing_and_picnic_advice(weather_info, llm_vendor)
    return weather_info, clothing_suggestions

# Button for retrieving weather and suggestions
if st.button("Get Weather and Advice"):
    weather_info, advice = process_weather_request(location, llm_vendor)

    # Display the weather information and suggestions
    st.write(f"**Weather in {weather_info['location']}:**")
    st.write(f"Temperature: {weather_info['temperature']}°C (Feels like {weather_info['feels_like']}°C)")
    st.write(f"Min Temp: {weather_info['temp_min']}°C, Max Temp: {weather_info['temp_max']}°C")
    st.write(f"Humidity: {weather_info['humidity']}%")
    st.write(f"Description: {weather_info['description']}")
    st.write("**Clothing Suggestions and Picnic Advice:**")
    st.write(advice)