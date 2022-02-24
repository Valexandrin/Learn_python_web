from flask import Flask
from weather import weather_by_city


app = Flask(__name__)

@app.route('/')
def index():
    weather = weather_by_city('Kazan')
    if weather:
        return 'Температура: {temp}, ощущается как: {feelslike}'.format(
            temp = weather['temp_C'],
            feelslike = weather['FeelsLikeC']
        )
    else:
        return 'Сервис погоды временно недоступен'

if __name__ == '__main__':
    app.run(debug=True)
