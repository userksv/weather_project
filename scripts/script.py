import requests
import os
from weather.models import Location

def req():
    API_KEY = os.getenv('API_KEY')
    lat = 37.5519
    lon = 126.9918
    city_name = 'Mosw'
    # url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}' # by coordinates
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}' # by city name
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err.response.status_code)
    # json_data = r.json()
    # print(json_data)
    # print(json_data['name'])
    # print(json_data['weather'][0]['main'])
    # print(json_data['weather'][0]['description'])
    # print(json_data['dt'])
    # print(json_data['main']['temp'])

def dt():
    import datetime
    timestamp = 1699244461
    print(datetime.datetime.fromtimestamp(timestamp))

def serialize_objects(objects):
    result = []
    for obj in objects:
        print(obj)
        result.append(obj)
    return result

req()
# print(serialize_objects(Location.objects.all().values()))