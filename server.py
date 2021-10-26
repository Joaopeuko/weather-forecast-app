import datetime
import json

from flask_caching import Cache
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from lib.openweather import OpenWeather

config = {
    "DEBUG": True,  # Some Flask-specific configurations..
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configuration.
    "CACHE_DEFAULT_TIMEOUT": 5 * 60  # Time, 60 seconds times 5.
}

app = Flask(__name__)  # It creates the Flask App
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_database.sqlite'
db = SQLAlchemy(app)  # Database handler.


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, unique=True, nullable=False)
    datetime_request = db.Column(db.String(80), unique=True, nullable=False)
    json_data = db.Column(db.String(), unique=False, nullable=False)

    def __init__(self, city_id, datetime_request, json_data):
        self.city_id = city_id
        self.datetime_request = datetime_request
        self.json_data = json_data


# It creates the database if do not exist.
# db.create_all()
# db.session.commit()


# Tell Flask to use the above-defined config
app.config.from_mapping(config)

cache = Cache(app)  # It handles the cache for the server-side.

weather = OpenWeather()  # It creates the class to handle Open Weather.


@app.route('/weather', methods=['POST'])
def results():
    """
    The function receives a for containing a city id and post it to database.
    :return: dict
        returns the status code.

    """
    city_id = request.form['city_id']
    result = weather.get_weather_by_city(city_id)

    weather_info = Weather(str(city_id), str(datetime.datetime.now().timestamp()), str(result))
    db.session.add(weather_info)
    db.session.commit()

    return {"status_code": '200'}


@app.route('/progress/<city_id>', methods=['GET'])
def progress(city_id):
    """
    These functions returns the number of information stored in the database to be used to calculate the progress
    in the front end.
    :return: json
        It returns a scalar containing the size of the database.
    """
    return json.dumps(db.session.query(Weather).count())


if __name__ == '__main__':
    app.run()  # It runs the server.
