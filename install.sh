#!/bin/bash

echo "📥 Installing Athan Player..."

# Create app directory
mkdir -p /home/$USER/athan
cp athan_player.py athan.mp3 /home/$USER/athan/

# Copy service file to systemd
sudo cp athan.service /etc/systemd/system/athan.service

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable athan.service
sudo systemctl start athan.service

echo "✅ Athan Player installed and running!"
echo "📂 Logs saved in /home/$USER/athan/athan_log.txt"
