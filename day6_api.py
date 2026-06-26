import requests

def get_weather(city):
    try:
        response = requests.get(f"https://wttr.in/{city}?format=j1")
        data = response.json()

        temp = data["current_condition"][0]["temp_C"]
        humidity = data["current_condition"][0]["humidity"]
        description = data["current_condition"][0]["weatherDesc"][0]["value"]

        print(f"\n{city} Weather Right Now:")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Condition: {description}")

    except:
        print("Something went wrong. Check your internet or city name!")

while True:
    city = input("\nEnter a city (or 'quit' to exit): ")
    if city == "quit":
        break
    get_weather(city)