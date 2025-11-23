#!/usr/bin/env bash

# Copy configuration files to respective locations
sudo cp ./98-touch-macropad.rules /etc/udev/rules.d/98-touch-macropad.rules
sudo cp ./touch-macropad-service.conf /etc/touch-macropad-service.conf
sudo cp ./touch-macropad-service.py /usr/local/bin/touch-macropad-service.py
sudo cp ./touch-macropad-service.service /etc/systemd/system/touch-macropad-service.service

# Set up systemd service file to run as currently logged-in user
sudo sed -i -e "s/ENTERUSER/$SUDO_USER/g" /etc/systemd/system/touch-macropad-service.service

# Reload udev rules
sudo udevadm control --reload

# Reload systemd manager configuration
sudo systemctl daemon-reload