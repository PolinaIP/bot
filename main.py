from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from bot.config import TOKEN, CHAT_ID, URL, SUBSTRING
import requests


def do_start(bot, update):
    bot.send_message(chat_id=CHAT_ID, text="Monitoring up")
    bot.send_message(chat_id=CHAT_ID, text="Для начала проверки введите любой символ")


def check_url(bot, update):
    response = requests.get(URL)
    if response.text == SUBSTRING:
        bot.send_message(chat_id=CHAT_ID, text='OK')
    else:
        bot.send_message(chat_id=CHAT_ID, text=f'{URL} is broken. {SUBSTRING} not found.')


def time(bot, update, job_queue):
    job = job_queue.run_repeating(check_url, 60)


def main():
    bot = Bot(token=TOKEN)
    updater = Updater(bot=bot)
    start_handler = CommandHandler("start", do_start)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(MessageHandler(None, time, pass_job_queue=True))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
