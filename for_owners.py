import datetime
from work_with_db import add_new_lost_animal

from telegram.ext import ConversationHandler


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


def description_of_lost_animal(update, context):
    day = int(str(update.message.text).split('-')[0])
    month = int(str(update.message.text).split('-')[1])
    year = int('20' + str(update.message.text).split('-')[2])
    context.user_data['date'] = datetime.date(year=year, month=month, day=day)
    update.message.reply_text("Опишите в нескольких предложениях Вашего питомца")
    print(context.user_data)
    return 3


def lost_place(update, context):
    context.user_data['description'] = update.message.text
    update.message.reply_text("Где Вы потеряли Вашего питомца? Напишите адрес этого места как можно точнее.")
    print(context.user_data)
    return 4


def owner_phone_number(update, context):
    context.user_data['place'] = update.message.text
    update.message.reply_text("Пожалуйста, отправьте боту свой номер телефона, чтобы нашедший смог с Вами связаться")
    return 5


def goodby_owner(update, context):
    context.user_data['phone_number'] = update.message.text
    update.message.reply_text("Ваше обращение записано. Надеемся, все будет хорошо. До свидания!")
    print(context.user_data)
    add_new_lost_animal(information_about_user=context.user_data)
    return ConversationHandler.END
