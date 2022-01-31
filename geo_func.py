import requests
from io import BytesIO
from PIL import Image


def get_toponym(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        return toponym
    return None


def get_coords(toponym_to_find):
    toponym = get_toponym(toponym_to_find)
    toponym_coodrinates = toponym["Point"]["pos"]
    if toponym_coodrinates:
        return toponym_coodrinates.split()
    return None, None


def find_store(address_ll):
    search_api_server = "https://search-maps.yandex.ru/v1/"

    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)

    if response:
        json_response = response.json()
        # Получаем первую найденную организацию.
        organization = json_response["features"][0]
        # Получаем координаты ответа.
        point = organization["geometry"]["coordinates"]
        return point


def show_map(type_map, point):
    params = {
        'l': type_map,
        'pt': point
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=params)

    Image.open(BytesIO(
        response.content)).show()