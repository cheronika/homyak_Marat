from data import db_session
from flask import Flask
from data.__all_models import Lost, Found

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/animals.sqlite")


def add_new_lost_animal(information_about_user):
    lost = Lost()
    lost.city = information_about_user['city']
    lost.lost_date = information_about_user['date']
    lost.lost_place = information_about_user['lost_place']
    lost.owner_phone = information_about_user['phone_number']
    lost.information = information_about_user['description']
    lost.stamp = information_about_user['stamp']
    lost.animal = information_about_user['animal']
    lost.collar = information_about_user['collar']
    lost.is_find = False
    db_session.global_init("db/animals.sqlite")
    db_sess = db_session.create_session()
    db_sess.add(lost)
    db_sess.commit()
    animal = db_sess.query(Lost).filter(Lost.city == information_about_user['city'],
                                        Lost.lost_date == information_about_user['date'],
                                        Lost.lost_place == information_about_user['lost_place'],
                                        Lost.owner_phone == information_about_user['phone_number'],
                                        Lost.information == information_about_user['description'],
                                        Lost.animal == information_about_user['animal'],
                                        Lost.stamp == information_about_user['stamp'],
                                        Lost.collar == information_about_user['collar']).first()
    peticion_number = animal.id
    return peticion_number


def add_new_found_animal(information_about_user):
    found = Found()
    found.city = information_about_user['city']
    found.found_date = information_about_user['date']
    found.found_place = information_about_user['found_place']
    found.finder_phone = information_about_user['phone_number']
    found.information = information_about_user['description']
    found.animal = information_about_user['animal']
    found.stamp = information_about_user['stamp']
    found.collar = information_about_user['collar']
    db_session.global_init("db/animals.sqlite")
    db_sess = db_session.create_session()
    db_sess.add(found)
    db_sess.commit()


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


if __name__ == '__main__':
    main()
