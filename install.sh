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

# update packages
sudo apt -y update

# install packages
sudo apt -y install jack_transport_link
sudo apt -y install rnbo-runner-panel
sudo apt -y install python3-smbus
sudo apt -y install puredata
sudo apt -y install git

# update everything and clean packages
sudo apt -y update
sudo apt -y upgrade
sudo apt -y clean
sudo apt -y autoremove
sudo apt -y autoclean

# clone repositories
cd ~
git clone --depth 1 https://github.com/cooperbaker/skronk
git clone --depth 1 https://github.com/cooperbaker/skronk-pd pd
echo ""

# update repositories
cd ~
cd skronk
pwd
git pull
chmod -v 755 skronk.py
echo ""
cd ~
cd pd
pwd
git pull
cd ~
echo ""

# enable i2c and spi
sudo raspi-config nonint do_i2c 1
sudo raspi-config nonint do_spi 1

# echo -e "\033[1mEnable I2C And SPI In The Raspi-Config Menus:"
# echo -e "\033[0m\033[1A"
# echo "  Interface Options → I2C → Yes"
# echo "  Interface Options → SPI → Yes"
# echo ""
# read -n 1 -r -s -p $'Press any key to run sudo raspi-config...\n'
# echo ""
# sudo raspi-config
# echo ""

# create system service
echo -e "\033[1mCreating Skronk Service"
echo -e "\033[0m\033[1A"
sudo systemctl disable skronk.service
sudo systemctl status skronk.service
sudo ln -sv /home/pi/skronk/skronk/skronk.service /etc/systemd/system/skronk.service
sudo systemctl enable skronk.service
echo ""

# goodbye
echo ""
echo -e "\033[1mSkronk Install Complete"
echo -e "\033[0m\033[1A"
echo ""

# read -n 1 -r -s -p $'Press any key to reboot...\n'
# sudo reboot now
# echo "reboot disabled"

#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
