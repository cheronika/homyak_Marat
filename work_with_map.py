import requests

from data.__all_models import Lost, Found
from work_with_db import db_session


def red_square_coords():  # получение координат Красной площади для того, чтобы нарисовать карту Москвы
    coords = requests.get(
        f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=Москва&format=json").json()[
        "response"]["GeoObjectCollection"]["featureMember"][
        0]["GeoObject"]["Point"]["pos"]
    longitude = coords.split()[0]
    lattitude = coords.split()[1]
    return longitude, lattitude


def lost_map(update, context):
    db_session.global_init("db/animals.sqlite")
    db_sess = db_session.create_session()
    pts = []
    for animal in db_sess.query(Lost).filter(Lost.city == "москва", Lost.lost_place != None, Lost.is_find == 0):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "format": "json",
            "geocode": animal.lost_place,
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b"
        }
        coords = requests.get(geocoder_api_server, params=geocoder_params).json()[
            "response"]["GeoObjectCollection"]["featureMember"][
            0]["GeoObject"]["Point"]["pos"]
        pt = ",".join([str(coords.split()[0]), str(coords.split()[1]), "pm2rdm"])
        pts.append(pt)
    pts = "~".join(pts)
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={red_square_coords()[0]},{red_square_coords()[1]}" \
                         f"&z=11&size=600,450&l=map&pt={pts}"
    context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption="на этой карте в виде красных меток отображены все потерянные в Москве питомцы :("
    )


def found_map(update, context):
    db_session.global_init("db/animals.sqlite")
    db_sess = db_session.create_session()
    pts = []
    for animal in db_sess.query(Found).filter(Found.city == "москва", Found.found_place != None):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "format": "json",
            "geocode": animal.found_place,
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b"
        }
        coords = requests.get(geocoder_api_server, params=geocoder_params).json()[
            "response"]["GeoObjectCollection"]["featureMember"][
            0]["GeoObject"]["Point"]["pos"]
        pt = ",".join([str(coords.split()[0]), str(coords.split()[1]), "pm2gnm"])
        pts.append(pt)
    pts = "~".join(pts)
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={red_square_coords()[0]},{red_square_coords()[1]}" \
                         f"&z=11&size=600,450&l=map&pt={pts}"
    context.bot.send_photo(
        update.message.chat_id,
        static_api_request,
        caption="на этой карте в виде зеленых меток отображены все найденные в Москве питомцы :))"
    )
