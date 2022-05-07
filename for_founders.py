import datetime
from work_with_db import add_new_found_animal

from telegram.ext import ConversationHandler


def i_found(update, context):  # функция начала диалога с человеком, который наашел животное
    update.message.reply_text("Так, опишите найденного питомца по пунктам "
                              "Если на какой-то вопрос Вы не можете или не хотите ответить, поставьте '-'. "
                              "Вы можете прервать Ваше обращение, написав боту '/stop', но тогда оно не будет записано")
    update.message.reply_text("В каком городе Вы находитесь?")
    return 1


def found_date(update, context):
    context.user_data['city'] = update.message.text
    update.message.reply_text("Когда Вы его нашли? Введите дату в формате дд-мм-гг")
    return 2


def description_of_found_animal(update, context):
    day = int(str(update.message.text).split('-')[0])
    month = int(str(update.message.text).split('-')[1])
    year = int('20' + str(update.message.text).split('-')[2])
    context.user_data['date'] = datetime.date(year=year, month=month, day=day)
    update.message.reply_text("Опишите в нескольких предложениях найденное животное")
    print(context.user_data)
    return 3


def found_place(update, context):
    context.user_data['description'] = update.message.text
    update.message.reply_text("Напишите адрес, где Вы нашли это животное, как можно точнее.")
    print(context.user_data)
    return 4


def founder_phone_number(update, context):
    context.user_data['place'] = update.message.text
    update.message.reply_text("Пожалуйста, отправьте боту свой номер телефона, "
                              "чтобы хозяин животного мог с Вами связаться.")
    return 5


def goodby_founder(update, context):
    context.user_data['phone_number'] = update.message.text
    update.message.reply_text("Ваше обращение записано. Надеемся, все будет хорошо. До свидания!")
    add_new_found_animal(information_about_user=context.user_data)
    return ConversationHandler.END
