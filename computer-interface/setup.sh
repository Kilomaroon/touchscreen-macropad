#!/usr/bin/env bash

# defaults
distro="ubuntu"
user=$SUDO_USER
group=$SUDO_USER

# get command-line flags
while getopts d:u:g: flag
do
    case $flag in
        d) distro=${OPTARG};;
        u) user=${OPTARG};;
        g) group=${OPTARG};;
        *) echo "Unknown option -{$flag}";;
    esac
done

# validate distribution
rules_file=""
if [[ "${distro,,}" == "arch" ]]; then
    echo "> Distribution: Arch"
    rules_file="72-touch-macropad-arch.rules"
elif [[ "${distro,,}" == "ubuntu" ]]; then
    echo "> Distribution: Ubuntu"
    rules_file="72-touch-macropad-ubuntu.rules"
else
    echo "Failed - '$distro' not a recognized value for '-d' flag, please use either 'arch' or 'ubuntu'."
    exit 1
fi

# validate user
if [[ "${user,,}" == "" || "${group,,}" == "" ]]; then
    echo "Failed - either this script was not run with sudo, or nothing was given for the 'user' and/or 'group' flag."
    exit 1
fi
echo "The systemd service will run as:"
echo "> User: $user"
echo "> User group: $group"

# get confirmation
read -p "Confirm? (y/n) : "
echo ${REPLY,,}
if [[ ! ${REPLY,,} =~ ^ye*s*$ ]]; then
    echo "Exiting..."
    exit 0
fi

# Copy configuration files to respective locations
sudo cp ./$rules_file /etc/udev/rules.d/72-touch-macropad.rules
echo "Created: /etc/udev/rules.d/72-touch-macropad.rules"

sudo cp ./touch-macropad-service.conf /etc/touch-macropad-service.conf
echo "Created: /etc/touch-macropad-service.conf"

sudo cp ./touch-macropad-service.py /usr/local/bin/touch-macropad-service.py
echo "Created: /usr/local/bin/touch-macropad-service.py"

sudo cp ./touch-macropad-service.service /etc/systemd/system/touch-macropad-service.service
echo "Created: /etc/systemd/system/touch-macropad-service.service"

# Set up systemd service file to run as currently logged-in user
sudo sed -i -e "s/ENTERUSER/$user/g" /etc/systemd/system/touch-macropad-service.service
sudo sed -i -e "s/ENTERGROUP/$group/g" /etc/systemd/system/touch-macropad-service.service

# Reload udev rules
sudo udevadm control --reload

# Reload systemd manager configuration
sudo systemctl daemon-reload

echo "Done!"