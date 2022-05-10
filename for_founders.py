import datetime
from work_with_db import add_new_found_animal

from telegram.ext import ConversationHandler


def i_found(update, context):
    update.message.reply_text("Так, опишите найденного питомца по пунктам "
                              "Если на какой-то вопрос Вы не можете или не хотите ответить, поставьте '-'. "
                              "Вы можете прервать Ваше обращение, написав боту '/stop', но тогда оно не будет записано")
    update.message.reply_text("В каком городе Вы находитесь?")
    return 1


def found_date(update, context):
    context.user_data['city'] = update.message.text
    update.message.reply_text("Когда Вы его нашли? Введите дату в формате дд-мм-гг")
    return 2


def f_what_animal(update, context):
    day = int(str(update.message.text).split('-')[0])
    month = int(str(update.message.text).split('-')[1])
    year = int('20' + str(update.message.text).split('-')[2])
    context.user_data['date'] = datetime.date(year=year, month=month, day=day)
    update.message.reply_text("Какое животное Вы нашли? Напишите его вид, например, собака, кошка или хомяк")
    return 3


def f_have_stamp(update, context):
    context.user_data['animal'] = update.message.text
    update.message.reply_text("Есть ли у этого животного клеймо? Ответьте 'да' или 'нет'")
    return 4


def f_have_collar(update, context):
    context.user_data['stamp'] = update.message.text.lower()
    if context.user_data['stamp'] == 'да':
        context.user_data['stamp'] = True
    else:
        context.user_data['stamp'] = False
    update.message.reply_text("Есть ли у этого животного ошейник? Ответьте 'да' или 'нет'")
    return 5


def found_place(update, context):
    context.user_data['collar'] = update.message.text.lower()
    if context.user_data['collar'] == 'да':
        context.user_data['collar'] = True
    else:
        context.user_data['collar'] = False
    update.message.reply_text("Напишите адрес, где Вы нашли это животное, как можно точнее.")
    return 6


def description_of_found_animal(update, context):
    context.user_data['found_place'] = update.message.text
    update.message.reply_text("Опишите в нескольких предложениях найденное животное")
    return 7


def founder_phone_number(update, context):
    context.user_data['description'] = update.message.text
    update.message.reply_text("Пожалуйста, отправьте боту свой номер телефона, "
                              "чтобы хозяин животного мог с Вами связаться.")
    return 9


def goodby_founder(update, context):
    context.user_data['phone_number'] = update.message.text
    update.message.reply_text("Ваше обращение записано. Надеемся, все будет хорошо. До свидания!")
    add_new_found_animal(information_about_user=context.user_data)
    return ConversationHandler.END
