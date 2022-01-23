import os
import telegram
import yaml

from mcstatus import MinecraftServer
from googleapiclient import discovery

server_ip = os.environ["SERVER_IP"]
server_project = os.environ["SERVER_PROJECT"]
server_zone = os.environ["SERVER_ZONE"]
server_name = os.environ["SERVER_NAME"]

service = discovery.build('compute', 'v1')
mc_server = MinecraftServer.lookup(server_ip)

# starter template code adapted from
# https://github.com/pabluk/serverless-telegram-bot/blob/master/main.py
bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])

def webhook(request):
    if request.method != "POST":
        return "ok"

    request_info = request.get_json(force=True)
    if request_info is None:
        return "ok"

    update = telegram.Update.de_json(request_info, bot)
    message = update.message

    try:
        # Reply with the same message
        chat_id = message.chat.id
        text = str(message.text)
    except AttributeError as e:
        return "ok"

    if text.startswith('/server '):
        command = text[text.index(' ') + 1:]

        if command == 'start':
            request = service.instances().start(
                project=server_project, zone=server_zone,
                instance=server_name
            )
            # response = request.execute()
            request.execute()
            bot.sendMessage(
                chat_id=chat_id, text='started server'
            )
        elif command == 'stop':
            num_players = 0
            try:
                status = mc_server.status()
                num_players = status.players.online
            except ConnectionRefusedError as e:
                pass

            if num_players > 0:
                bot.sendMessage(
                    chat_id=chat_id,
                    text=f'server has {num_players} players'
                )
            else:
                request = service.instances().stop(
                    project=server_project, zone=server_zone,
                    instance=server_name
                )
                request.execute()
                bot.sendMessage(
                    chat_id=chat_id, text='stopped server'
                )
        else:
            bot.sendMessage(
                chat_id=chat_id,
                text=f'unknown command [{command}]'
            )

    return "ok"