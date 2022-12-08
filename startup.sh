#!/bin/bash
mount /dev/sdb /home/minecraft
cd /home/minecraft
tmux new-session -d -s minecraft "sudo java -Xmx1024M -Xms1024M -jar server.jar nogui"
tmux new-session -d -s smart_shutdown "python3.8 code/smart_shutdown.py"
