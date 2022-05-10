import datetime

from telegram.ext import ConversationHandler

from work_with_db import add_new_lost_animal
from work_with_map import found_in_radius

found_animals_in_radius = []


def i_lost(update, context):
    update.message.reply_text("Так, опишите своего питомца по пунктам. "
                              "Если на какой-то вопрос Вы не можете или не хотите ответить, поставьте '-'. "
                              "Вы можете прервать Ваше обращение, написав боту '/stop', но тогда оно не будет записано")
    update.message.reply_text("В каком городе находитесь Вы и Ваш питомец?")
    return 1


def lost_date(update, context):
    context.user_data['city'] = update.message.text
    update.message.reply_text("Когда Вы его потеряли? Введите дату в формате дд-мм-гг")
    return 2


def l_what_animal(update, context):
    day = int(str(update.message.text).split('-')[0])
    month = int(str(update.message.text).split('-')[1])
    year = int('20' + str(update.message.text).split('-')[2])
    context.user_data['date'] = datetime.date(year=year, month=month, day=day)
    update.message.reply_text("Какое животное Вы потеряли? Напишите название вида (например, собака, кошка или хомяк)")
    return 3


def l_have_stamp(update, context):
    context.user_data['animal'] = update.message.text
    update.message.reply_text("Есть ли у Вашего питомца клеймо? Ответьте 'да' или 'нет'")
    return 4


def l_have_collar(update, context):
    context.user_data['stamp'] = update.message.text.lower()
    if context.user_data['stamp'] == 'да':
        context.user_data['stamp'] = True
    else:
        context.user_data['stamp'] = False
    update.message.reply_text("Есть ли у Вашего питомца ошейник? Ответьте 'да' или 'нет'")
    return 5


def lost_place(update, context):
    context.user_data['collar'] = update.message.text.lower()
    if context.user_data['collar'] == 'да':
        context.user_data['collar'] = True
    else:
        context.user_data['collar'] = False
    update.message.reply_text("Где Вы потеряли Вашего питомца? Напишите адрес этого места как можно точнее.")
    update.message.reply_text("А я проверю по базе найденных животных, не нашел ли его кто-то.")
    print(context.user_data)
    return 6


def radius(update, context):
    context.user_data['lost_place'] = update.message.text
    update.message.reply_text(
        "На каком расстоянии от места потери (км) мне поискать найденных животных? Введите только число")
    return 7


def search_in_db(update, context):
    global found_animals_in_radius

    r = int(update.message.text)
    found_animals_in_radius = found_in_radius(context.user_data['date'], context.user_data['lost_place'],
                                              context.user_data['animal'], context.user_data['stamp'],
                                              context.user_data['collar'], r)
    if len(found_animals_in_radius) == 0:
        update.message.reply_text(f"К сожалению в радиусе {r} км никаких животных пока не нашли.")
        update.message.reply_text("Давайте я запишу Ваше обращение, и с Вами свяжутся, если что-нибудь найдут")
        update.message.reply_text(
            "Если Вы не хотите продолжать запись обращения, отправьте мне /stop, а если хотите - любой другой символ")
    else:
        update.message.reply_text(f"В радиусе {r} км найдено животных: {len(found_animals_in_radius)}")
        update.message.reply_text("Сейчас я выведу информацию о них")
        for i in range(len(found_animals_in_radius)):
            update.message.reply_text(f"Найденный питомец номер {i + 1}")
            update.message.reply_text(f"Животное: {found_animals_in_radius[i]['animal']}")
            if found_animals_in_radius[i]['stamp']:
                update.message.reply_text("Клеймо: есть")
            else:
                update.message.reply_text("Клеймо: нет")
            if found_animals_in_radius[i]['collar']:
                update.message.reply_text("Ошейник: есть")
            else:
                update.message.reply_text("Ошейник: нет")
            update.message.reply_text(f"Описание: {found_animals_in_radius[i]['information']}")
            update.message.reply_text(f"Где найден: {found_animals_in_radius[i]['found_place']}")
            update.message.reply_text(f"Когда найден: {found_animals_in_radius[i]['found_date']}")
            update.message.reply_text(f"Телефон нашедшего: {found_animals_in_radius[i]['founder_phone']}")
        update.message.reply_text("Если Вам кажется, что один из этих питомцев Ваш, смело пишите нашедшему!")
        update.message.reply_text("Диалог со мной можно остановить, отправив мне команду /stop")
        update.message.reply_text("Если же ни одно из животных Вам не кажется подходящим, продолжите Ваше обращение, "
                                  "и я его запишу, чтобы с вами связались, когда Вашего питомца найдут")
        update.message.reply_text("Чтобы продолжить, отправьте мне любой символ, кроме команды /stop")
    return 8


def description_of_lost_animal(update, context):
    update.message.reply_text("Опишите в нескольких предложениях Вашего питомца")
    print(context.user_data)
    return 9


def owner_phone_number(update, context):
    context.user_data['description'] = update.message.text
    update.message.reply_text("Пожалуйста, отправьте боту свой номер телефона, чтобы нашедший смог с Вами связаться")
    return 11


def goodby_owner(update, context):
    context.user_data['phone_number'] = update.message.text
    print(context.user_data)
    peticion_number = add_new_lost_animal(information_about_user=context.user_data)
    update.message.reply_text(
        f"Ваше обращение записано. ID обращения: {peticion_number}. Надеемся, все будет хорошо. До свидания!")
    return ConversationHandler.END
