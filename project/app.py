import requests
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

## OpenWeatherMap API key
api_key = '[Insert API key here]'

## City search
@app.route('/', methods=['GET', 'POST'])
def city_search():
    if request.method == 'POST':
        city = request.form['city']
        if city:
            return redirect(url_for('weather', city=city))
    return render_template('index.html')

## City weather
@app.route('/weather/<city>')
def weather(city):
    rain_data = get_rain_forecast(city)
    if rain_data:
        will_rain = check_rain_forecast(rain_data)
        return render_template('weather.html', city=city, will_rain=will_rain)
    else:
        return render_template('not-found.html')

## Get weather forecast data from OpenWeatherMap
def get_rain_forecast(city):
    base_url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    return None

## Check if result includes rain or drizzle for current day
def check_rain_forecast(rain_data):
    today_date = datetime.now().strftime('%Y-%m-%d')

    for forecast in rain_data['list']:
        forecast_date = forecast['dt_txt'].split()[0]
        if forecast_date == today_date:
            weather = forecast['weather'][0]['main'].lower()
            if 'rain' in weather or 'drizzle' in weather:
                return True
    return False

if __name__ == '__main__':
    app.run(debug=True)