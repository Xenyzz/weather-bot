import requests
import dotenv
from os import getenv

dotenv.load_dotenv()
API_key = getenv("API_WEATHER_KEY")


def get_geo(city: str) -> tuple | None:
    city_name = city
    limit = 1
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={API_key}"
    response = requests.get(url)
    if response.status_code == 200:
        city_data = response.json()
        if city_data:
            return city_data[0]['lat'], city_data[0]['lon']
        return None
    print(response.status_code, response.text)
    return None


def get_weather(city: str) -> dict | None:
    city_data = get_geo(city)
    if not city_data:
        print("non-existent city")
        return None
    lat, lon = city_data

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}"
    response = requests.get(url)
    if response.status_code == 200:
        gotten_weather = response.json()
        weather = gotten_weather["weather"][0]["main"]
        temp_kelvin = gotten_weather["main"]["temp"]
        temp_celsius = temp_kelvin - 273.15
        return {
            'weather': weather,
            'temp': f"{temp_celsius:.0f}°C",
            'city': city
        }
    print(response.status_code, response.text)
    return None


if __name__ == "__main__":
    print(get_weather("Daugavpils"))
