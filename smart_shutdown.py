import os
import time
import traceback

from datetime import datetime
from mcstatus import MinecraftServer

try:
    lookup_delay = 20
    shutdown_wait = 30 * 60
    server = MinecraftServer.lookup("localhost")
    last_online_timestamp = time.time()

    while True:
        num_players = 0
        time_now = time.time()
        utc_time = datetime.utcfromtimestamp(time_now)
        formatted = utc_time.strftime("%Y-%m-%d %H:%M:%S")
        print(f'time now is {formatted} UTC')

        try:
            status = server.status()
            num_players = status.players.online
        except (ConnectionRefusedError, ConnectionResetError) as e:
            pass

        if num_players > 0:
            last_online_timestamp = time_now

        empty_duration = time_now - last_online_timestamp
        print(f'shutdown wait: {shutdown_wait}')

        if empty_duration >= shutdown_wait:
            print(f'no players detected for {empty_duration:.2f}s')
            print('shutting down now')
            os.system('sudo ./backup.sh')
            os.system('sudo shutdown now')
        else:
            print(f'no players detected for {empty_duration:.2f}s')
            print(f'players online: {num_players}')

        time.sleep(lookup_delay)

except Exception as e:
    print(traceback.format_exc())
    input('SHUTDOWN SCRIPT FAILED >>> ')
    raise e