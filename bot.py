import os
import telegram

# starter template code adapted from
# https://github.com/pabluk/serverless-telegram-bot/blob/master/main.py
bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])

def webhook(request):
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        # Reply with the same message
        bot.sendMessage(chat_id=chat_id, text=update.message.text)

    return "ok"