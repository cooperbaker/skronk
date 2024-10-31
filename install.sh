#!/bin/bash
#-------------------------------------------------------------------------------
# install.sh
#
# Skronk Install Script For RNBO Raspbian OS Image
#
# 1. Follow skronk sd card flashing instructons URL
# 2. Run this raspberry pi command to install skronk:
# $  curl https://raw.githubusercontent.com/cooperbaker/skronk/refs/heads/main/install.sh | bash
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------

# hello
sudo echo ""
echo -e "\033[1mInstalling Skronk"
echo -e "\033[0m\033[1A"
echo ""

# go home
cd ~

# update packages
sudo apt -y update

# install packages
sudo apt -y install jack_transport_link
sudo apt -y install rnbo-runner-panel
sudo apt -y install python3-smbus
sudo apt -y install puredata
sudo apt -y install git

# update everything and clean packages
sudo apt -y update && sudo apt -y upgrade
sudo apt -y clean
sudo apt -y autoremove
sudo apt -y autoclean

# clone repositories
git clone --depth 1 https://github.com/cooperbaker/skronk
chmod -v 755 ./skronk/skronk.py
# git clone --depth 1 https://github.com/cooperbaker/skronk-pd pd
echo ""

# enable i2c and spi
echo -e "\033[1mEnable I2C And SPI In The Raspi-Config Menus:"
echo -e "\033[0m\033[1A"
echo "  Interface Options → I2C → Yes"
echo "  Interface Options → SPI → Yes"
echo ""
read -rsp $'Press any key to run "sudo raspi-config"...\n' -n1 key
sudo raspi-config
echo ""

# paswordless sudo
echo -e "\033[1mEdit /etc/sudoers For Passwordless Sudo"
echo -e "\033[0m\033[1A"
echo "  paste the following line at the end:"
echo "  pi ALL=(ALL) NOPASSWD: ALL"
echo ""
read -rsp $'Press any key to run "sudo visudo"...\n' -n1 key
sudo visudo
echo ""

# create system service
echo -e "\033[1mCreating Skronk Service"
echo -e "\033[0m\033[1A"
sudo ln -sv /home/pi/skronk/skronk/skronk.service /etc/systemd/system/skronk.service
sudo systemctl enable skronk.service
echo ""

# goodbye
echo ""
echo -e "\033[1mSkronk Install Complete"
echo -e "\033[0m\033[1A"
echo ""

read -rsp $'Press any key to continue...\n' -n1 key

#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------