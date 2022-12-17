import os
import re
import socket
import telegram
import yaml
import traceback

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


def is_server_running():
    request = service.instances().list(
        project=server_project, zone=server_zone,
        filter='status=running'
    )

    servers_list = request.execute()
    is_running = 'items' in servers_list
    return is_running


def handle_server_commands(message, command):
    if command == 'start':
        request = service.instances().start(
            project=server_project, zone=server_zone,
            instance=server_name
        )
        # response = request.execute()
        request.execute()
        message.reply_text(text='started server')
        return True

    elif command == 'status':
        is_running = is_server_running()

        if is_running:
            message.reply_text('Server is running')
        else:
            message.reply_text('Server is not running')

    elif command == 'stop':
        is_running = is_server_running()

        if not is_running:
            message.reply_text('Server instance is off already')
            return False

        try:
            status = mc_server.status()
            num_players = status.players.online
        except ConnectionRefusedError as e:
            message.reply_text('Failed to connect to MC server')
            return False
        except BrokenPipeError as e:
            message.reply_text('Broken pipe while reading server status')
            return False
        except socket.timeout as e:
            message.reply_text('Socket timeout while reading server status')
            return False

        if num_players > 0:
            message.reply_text(
                text=f'server has {num_players} players omo'
            )
        else:
            request = service.instances().stop(
                project=server_project, zone=server_zone,
                instance=server_name
            )
            request.execute()
            message.reply_text(text='stopped server')

    else:
        message.reply_text(
            text=f'unknown command [{command}]'
        )


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
        text = str(message.text)
    except AttributeError as e:
        return "ok"

    try:
        if text.startswith('/server '):
            command = text[text.index(' ') + 1:]
            handle_server_commands(message, command)

    except Exception as e:
        message.reply_text('WEBHOOK HANDLE ERROR')
        err_msg = traceback.format_exc()
        print(err_msg)

    return "ok"