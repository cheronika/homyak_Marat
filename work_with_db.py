from data import db_session
from flask import Flask
from data.__all_models import Lost, Found
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/animals.sqlite")


def add_new_lost_animal(information_about_user):
    lost = Lost()
    lost.city = information_about_user['city']
    lost.lost_date_and_time = information_about_user['date']
    lost.lost_place = information_about_user['place']
    lost.owner_phone = information_about_user['phone_number']
    lost.information = information_about_user['description']
    lost.is_find = False
    db_session.global_init("db/animals.sqlite")
    db_sess = db_session.create_session()
    db_sess.add(lost)
    db_sess.commit()


def add_new_found_animal(information_about_user):
    found = Found()
    found.city = information_about_user['city']
    found.found_date = information_about_user['date']
    found.found_place = information_about_user['place']
    found.finder_phone = information_about_user['phone_number']
    found.information = information_about_user['description']
    db_session.global_init("db/animals.sqlite")
    db_sess = db_session.create_session()
    db_sess.add(found)
    db_sess.commit()


if __name__ == '__main__':
    main()
