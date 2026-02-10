#!/usr/bin/env bash

help="""
Bash script that sets up the files for the touchscreen macropad.

Usage:

    bash setup.sh -u myuser -g mygroup -d (arch|ubuntu)

Options:

    -u : The user that the systemd service will run as. Defaults to the name of the user that ran the script.

    -g : The group of the user that the systemd service will run as. Defaults to the name of the user that ran the script.
    
    -d : The distribution. Supported distros are 'arch' and 'ubuntu', though others may also work (check the 72-touch-macropad-*.rules files to see the difference)
    
    -h : Displays this message :)
"""

# defaults
distro="ubuntu"
user=$SUDO_USER
userid=`id -u $user`
group=$SUDO_USER

# get command-line flags
while getopts d:u:g:h flag
do
    case $flag in
        d) distro=${OPTARG};;
        u) user=${OPTARG};;
        g) group=${OPTARG};;
        h) echo "$help" && exit 0 ;;
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

mkdir /usr/local/bin/touch-macropad
sudo cp -r ./touch-macropad-service/. /usr/local/bin/touch-macropad
echo "Created: /usr/local/bin/touch-macropad/*"
# fix permissions
sudo chown -R $user:$group /usr/local/bin/touch-macropad
sudo chmod u+x /usr/local/bin/touch-macropad

sudo cp ./touch-macropad-service.service /etc/systemd/user/touch-macropad-service.service
echo "Created: /etc/systemd/system/touch-macropad-service.service"

# Set up systemd service file to run as currently logged-in user
sudo sed -i -e "s/ENTERUSER/$user/g" /etc/systemd/user/touch-macropad-service.service
sudo sed -i -e "s/ENTERGROUP/$group/g" /etc/systemd/user/touch-macropad-service.service
# Set up directories so that current user's pipewire files are exposed to service
sudo sed -i -e "s/ENTERUID/$userid/g" /etc/systemd/user/touch-macropad-service.service

# Reload udev rules
sudo udevadm control --reload

# Reload systemd manager configuration
systemctl --user daemon-reload
# i use this script to for quickly reloading stuff after making changes and this is helpful
systemctl --user restart touch-macropad-service

echo "Done!"
