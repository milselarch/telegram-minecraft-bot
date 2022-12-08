#!/bin/bash
sudo tmux send -t minecraft.0 " " ENTER
sudo tmux send -t minecraft.0 "/save-all" ENTER
:sudo tmux send -t minecraft.0 "/save-off" ENTER
sudo tmux send -t minecraft.0 " " ENTER
sudo tmux send -t minecraft.0 "/stop" ENTER
/usr/bin/gsutil cp -R /home/minecraft/world gs://minecraft_gcp_telegram_backups/$(date "+%Y%m%d-%H%M%S")-world
sudo shutdown now
