import logging
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler
from for_owners import i_lost, lost_date, description_of_lost_animal, lost_place, owner_phone_number, goodby_owner, \
    search_in_db, radius, l_have_stamp, l_have_collar, l_what_animal
from for_founders import i_found, found_date, description_of_found_animal, found_place, founder_phone_number, \
    goodby_founder, f_have_stamp, f_have_collar, f_what_animal
from work_with_map import lost_map, found_map
from for_stop_searching import stop_searching, cancel_searching

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = "5348701239:AAF5RFIr4Fng7UCcbYQRT_xLcg_O5aVflhc"

information_about_user = {} 


def start(update, context):
    update.message.reply_text("Привет! Я бот для поиска пропавших животных.", reply_markup=markup)


def help(update, context):
    update.message.reply_text(
        "Тут будет написано, как со мной работать")


reply_keyboard = [['/i_lost'],
                  ['/i_found'],
                  ['/stop_searching'],
                  ['/map_1'],
                  ['/map_2']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def map_1(update, context):
    lost_map(update, context)


def map_2(update, context):
    found_map(update, context)


def stop(update, context):
    update.message.reply_text("Ваше обращение НЕ записано. Надеемся, что с питомцем все будет хорошо! До свидания!")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("map_1", map_1))
    dp.add_handler(CommandHandler("map_2", map_2))
    dp.add_handler(CommandHandler("close", close_keyboard))
    conv_handler_1 = ConversationHandler(
        entry_points=[CommandHandler('i_lost', i_lost)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, lost_date, pass_user_data=True)],
            2: [MessageHandler(Filters.text & ~Filters.command, l_what_animal, pass_user_data=True)],
            3: [MessageHandler(Filters.text & ~Filters.command, l_have_stamp, pass_user_data=True)],
            4: [MessageHandler(Filters.text & ~Filters.command, l_have_collar, pass_user_data=True)],
            5: [MessageHandler(Filters.text & ~Filters.command, lost_place, pass_user_data=True)],
            6: [MessageHandler(Filters.text & ~Filters.command, radius, pass_user_data=True)],
            7: [MessageHandler(Filters.text & ~Filters.command, search_in_db, pass_user_data=True)],
            8: [MessageHandler(Filters.text & ~Filters.command, description_of_lost_animal, pass_user_data=True)],
            9: [MessageHandler(Filters.text & ~Filters.command, owner_phone_number, pass_user_data=True)],
            # 10: [MessageHandler(Filters.text & ~Filters.command, add_photo, pass_user_data=True)],
            11: [MessageHandler(Filters.text & ~Filters.command, goodby_owner, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler_1)
    conv_handler_2 = ConversationHandler(
        entry_points=[CommandHandler('i_found', i_found)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, found_date, pass_user_data=True)],
            2: [MessageHandler(Filters.text & ~Filters.command, f_what_animal, pass_user_data=True)],
            3: [MessageHandler(Filters.text & ~Filters.command, f_have_stamp, pass_user_data=True)],
            4: [MessageHandler(Filters.text & ~Filters.command, f_have_collar, pass_user_data=True)],
            5: [MessageHandler(Filters.text & ~Filters.command, found_place, pass_user_data=True)],
            6: [MessageHandler(Filters.text & ~Filters.command, description_of_found_animal, pass_user_data=True)],
            7: [MessageHandler(Filters.text & ~Filters.command, founder_phone_number, pass_user_data=True)],
            # 8: [MessageHandler(Filters.text & ~Filters.command, f_add_photo, pass_user_data=True)],
            9: [MessageHandler(Filters.text & ~Filters.command, goodby_founder, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler_2)
    conv_handler_3 = ConversationHandler(
        entry_points=[CommandHandler('stop_searching', stop_searching)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, cancel_searching)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler_3)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
