from flask import Flask, request
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <html>
        <body>
            <h1>Weather App 🌤️</h1>
            <form action="/weather" method="get">
                <input type="text" name="city" placeholder="Enter a city">
                <button type="submit">Get Weather</button>
            </form>
        </body>
    </html>
    """


@app.route("/weather")
def weather():
    city = request.args.get("city")
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    data = response.json()

    temp = data["current_condition"][0]["temp_C"]
    humidity = data["current_condition"][0]["humidity"]
    description = data["current_condition"][0]["weatherDesc"][0]["value"]

    return f"""
    <html>
        <body>
            <h1>{city} Weather 🌤️</h1>
            <p>Temperature: {temp}°C</p>
            <p>Humidity: {humidity}%</p>
            <p>Condition: {description}</p>
            <a href="/">Search another city</a>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)