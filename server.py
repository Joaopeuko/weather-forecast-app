import datetime
import json
import sqlite3
from flask_caching import Cache
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from lib.openweather import OpenWeather

config = {
    "DEBUG": True,  # Some Flask-specific configurations..
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configuration.
    "CACHE_DEFAULT_TIMEOUT": 5 * 60  # Time, 60 seconds times 5.
}

app = Flask(__name__)  # It creates the Flask App

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_database.sqlite'
# app.config['SQLALCHEMY_POOL_SIZE'] = 5
db = SQLAlchemy(app)


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, unique=True, nullable=False)
    datetime_request = db.Column(db.String(80), unique=True, nullable=False)
    json_data = db.Column(db.String(), unique=False, nullable=False)

    def __init__(self, city_id, datetime_request, json_data):
        self.city_id = city_id
        self.datetime_request = datetime_request
        self.json_data = json_data

    def __repr__(self):
        return '<User %r>' % self.username


db.create_all()
db.session.commit()


# Tell Flask to use the above-defined config
app.config.from_mapping(config)

cache = Cache(app)  # It handles the cache for the server-side.

weather = OpenWeather()  # It creates the class to handle Open Weather.


@app.route('/weather', methods=['POST'])
def results():
    """
    The function receives a string containing a city name and returns the weather information.
    Also, it caches the information.
    :param city_name: str
        It receives a request from the front end containing a city name.
    :return: dict
        returns a dictionary containing information about the weather of a determined city.

    """
    city_id = request.form['city_id']
    result = weather.get_weather_by_city(city_id)

    if result['city'] == 'city_name_invalid':
        abort(404)  # In case the city name is invalid it returns an error 404.

    weather_info = Weather(str(city_id), str(datetime.datetime.now().timestamp()), str(result))
    db.session.add(weather_info)
    db.session.commit()

    return '200'


@app.route('/weather', methods=['GET'])
def max_values():
    """
    These functions handle the max amount of information needed to be returned to the user from the cached information.
    If the amount of information
    :return: json
        It returns a JSON that contains a dictionary about the last results.
    """

    if 'max' in list(request.args.keys()) and request.args['max'].isnumeric():
        max_number = int(request.args['max'])  # It returns the new amount of information the users requested.
    else:
        max_number = 5  # The default amount of data returned.

    result = []
    # It retrieves the newest amount of data requested.
    for key in reversed(list(cache.cache._cache.keys())[-max_number:]):
        result.append(cache.get(key))
    return json.dumps(result)


if __name__ == '__main__':
    app.run()  # It runs the server.
