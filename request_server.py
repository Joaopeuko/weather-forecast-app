import json
import requests
from time import sleep

URL = 'http://host.docker.internal:5000'

with open('city_ids.json', 'r') as j:
    city_ids = json.loads(j.read())

for id_ in city_ids['city_ids']:
    payload = {'city_id': id_}
    result = requests.post(url=URL + '/weather', data=payload).text
    result_get = requests.get(url=URL + f'/progress/{id_}')
    print(f'\r Progress: '
          f'{result_get.json()}/{len(city_ids["city_ids"])} '
          f'({100*(result_get.json()/len(city_ids["city_ids"])):.2f}%).', end="")

    sleep(1)


