import telebot
import os
from flask import Flask, request
import logging

bot = telebot.TeleBot('1022635227:AAEi2woyfX_SWvKlpztyWHOHM-RIVIeFids')


# Здесь пишем наши хэндлеры
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}.')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'hui', parse_mode="Markdown")


# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)


    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200


    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(
            url="https://min-gallows.herokuapp.com/bot")  # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200


    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)
