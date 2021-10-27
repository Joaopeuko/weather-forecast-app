import json
import responses
import requests

SERVER_URL = 'http://127.0.0.1:5000'


# All the functions below try to anticipate the problems that might appear when using the
# two functions that call the server.

# City Name ---
# - More than 60 request in one minute
# - Invalid ID
# - Valid ID


@responses.activate
def test_rate_limit():
    responses.add(responses.GET, 'http://127.0.0.1:5000/weather', status=429)
    resp = requests.get('http://127.0.0.1:5000/weather')

    assert resp.status_code == 429


def test_valid_id():
    payload = {'city_id': 3441292}
    result = requests.post(url='http://127.0.0.1:5000/weather', data=payload).text
    assert result == '200'


def test_invalid_id():
    payload = {'city_id': 'flopers'}
    assert isinstance(requests.post(url='http://127.0.0.1:5000/weather', data=payload).text, str)


# Progress ---
#   - Will return always a number

def test_progress_number():
    result_get = requests.get(url=f'http://127.0.0.1:5000/progress/{123}')
    assert isinstance(result_get.status_code, int)


if __name__ == '__main__':
    ...
    # Run the server to be able to test the functions.

    # # City id:
    test_rate_limit()
    test_valid_id()
    test_invalid_id()
    # -----
    # Progress:
    test_progress_number()
