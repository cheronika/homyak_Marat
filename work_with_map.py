import requests

from data.__all_models import Lost, Found
from work_with_db import db_session
from distance import lonlat_distance


def red_square_coords():  # координаты Москвы
    coords = requests.get(
        f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=Москва&format=json").json()[
        "response"]["GeoObjectCollection"]["featureMember"][
        0]["GeoObject"]["Point"]["pos"]
    longitude = coords.split()[0]
    lattitude = coords.split()[1]
    return longitude, lattitude


def coords_from_address(address):  # преобразование полученного адреса в координаты
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "format": "json",
        "geocode": address,
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b"
    }
    coords = requests.get(geocoder_api_server, params=geocoder_params).json()[
        "response"]["GeoObjectCollection"]["featureMember"][
        0]["GeoObject"]["Point"]["pos"]
    return coords


def lost_map(update, context):  # карта потерянных животных
    db_session.global_init("db/animals.sqlite")
    db_sess = db_session.create_session()
    pts = []
    for animal in db_sess.query(Lost).filter(Lost.city == "москва", Lost.lost_place != None, Lost.is_find == 0):
        coords = coords_from_address(animal.lost_place)
        pt = ",".join([str(coords.split()[0]), str(coords.split()[1]), "pm2rdm"])
        pts.append(pt)
    pts = "~".join(pts)
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={red_square_coords()[0]},{red_square_coords()[1]}" \
                         f"&z=10&size=600,450&l=map&pt={pts}"
    context.bot.send_photo(
        update.message.chat_id,
        static_api_request,
        caption="на этой карте в виде красных меток отображены все потерянные в Москве питомцы :("
    )


def found_map(update, context):  # карта найденных животных
    db_session.global_init("db/animals.sqlite")
    db_sess = db_session.create_session()
    pts = []
    for animal in db_sess.query(Found).filter(Found.city == "москва", Found.found_place != None):
        coords = coords_from_address(animal.found_place)
        pt = ",".join([str(coords.split()[0]), str(coords.split()[1]), "pm2gnm"])
        pts.append(pt)
    for animal in db_sess.query(Lost).filter(Lost.city == "москва", Lost.lost_place != None, Lost.is_find == 1):
        coords = coords_from_address(animal.lost_place)
        pt = ",".join([str(coords.split()[0]), str(coords.split()[1]), "pm2gnm"])
        pts.append(pt)
    pts = "~".join(pts)
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={red_square_coords()[0]},{red_square_coords()[1]}" \
                         f"&z=10&size=600,450&l=map&pt={pts}"
    context.bot.send_photo(
        update.message.chat_id,
        static_api_request,
        caption="на этой карте в виде зеленых меток отображены все найденные в Москве питомцы :))"
    )


def found_in_radius(date, address, kind, stamp, collar, radius):
    # находит по бд подходящих животных, найденных на указанном пользователем расстоянии от места потери
    db_session.global_init("db/animals.sqlite")
    db_sess = db_session.create_session()
    coords = coords_from_address(address)
    coords = float(coords.split()[0]), float(coords.split()[1])
    animals = []
    for animal in db_sess.query(Found).filter(Found.found_place != None, Found.found_date > date, Found.animal == kind,
                                              Found.stamp == stamp, Found.collar == collar):
        d = {}
        coords_2 = coords_from_address(str(animal.city) + str(animal.found_place))
        coords_2 = float(coords_2.split()[0]), float(coords_2.split()[1])
        if int(lonlat_distance(coords, coords_2)) < (radius * 1000):
            d['id'] = animal.id
            d['city'] = animal.city
            d['found_place'] = animal.found_place
            d['founder_phone'] = animal.finder_phone
            d['found_date'] = animal.found_date
            d['information'] = animal.information
            d['animal'] = animal.animal
            d['stamp'] = animal.stamp
            d['collar'] = animal.collar
            animals.append(d)
    return animals
