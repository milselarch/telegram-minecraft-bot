#!/bin/bash
sudo tmux send -t minecraft.0 " " ENTER
sudo tmux send -t minecraft.0 "/save-all" ENTER
/usr/bin/gsutil cp -R ./world gs://minecraft_gcp_telegram_backups/$(date "+%Y%m%d-%H%M%S")-world
