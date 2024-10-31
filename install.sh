#!/bin/bash
#-------------------------------------------------------------------------------
# install.sh
#
# Skronk Install Script For RNBO Raspbian OS Image
#
# 1. Follow skronk sd card flashing instructons in README.md
# 2. Run this command from a fresh os image to install skronk:
# $  curl https://raw.githubusercontent.com/cooperbaker/skronk/refs/heads/main/install.sh | bash
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# install skronk
#-------------------------------------------------------------------------------
sudo echo ""
echo -e "\033[1mInstalling Skronk"
echo -e "\033[0m\033[1A"
echo ""

#-------------------------------------------------------------------------------
# update packages
#-------------------------------------------------------------------------------
echo -e "\033[1mUpdating Package Lists..."
echo -e "\033[0m\033[1A"
echo ""
sudo apt -y update
echo ""

#-------------------------------------------------------------------------------
# install packages
#-------------------------------------------------------------------------------
echo -e "\033[1mInstalling Packages..."
echo -e "\033[0m\033[1A"
echo ""
sudo apt -y install jack_transport_link
sudo apt -y install rnbo-runner-panel
sudo apt -y install python3-smbus
sudo apt -y install puredata
sudo apt -y install git
echo""

#-------------------------------------------------------------------------------
# upgrade packages
#-------------------------------------------------------------------------------
echo -e "\033[1mUpgrading Packages..."
echo -e "\033[0m\033[1A"
echo ""
sudo apt -y update
sudo apt -y upgrade
sudo apt -y clean
sudo apt -y autoremove
sudo apt -y autoclean
echo""

#-------------------------------------------------------------------------------
# install skronk library
#-------------------------------------------------------------------------------
echo -e "\033[1mInstalling Skronk Library..."
echo -e "\033[0m\033[1A"
echo ""
cd ~
sudo rm -r skronk
git clone --depth 1 https://github.com/cooperbaker/skronk
rm -v ./skronk/install.sh
chmod -v 755 ./skronk/skronk.py
echo ""

#-------------------------------------------------------------------------------
# install skronk-pd library
#-------------------------------------------------------------------------------
# echo -e "\033[1mInstalling Skronk-Pd Library"
# echo -e "\033[0m\033[1A"
# echo ""
# cd ~
# sudo rm -r pd
# git clone --depth 1 https://github.com/cooperbaker/skronk-pd pd

# # update
# cd pd
# pwd
# git pull
# cd ~
# echo ""

#-------------------------------------------------------------------------------
# enable i2c and spi
#-------------------------------------------------------------------------------
echo -e "\033[1mEnabling I2C and SPI..."
echo -e "\033[0m\033[1A"
echo ""
echo "sudo raspi-config nonint do_i2c 0"
sudo raspi-config nonint do_i2c 0
echo "sudo raspi-config nonint do_spi 0"
sudo raspi-config nonint do_spi 0
echo ""

#-------------------------------------------------------------------------------
# create system service
#-------------------------------------------------------------------------------
echo -e "\033[1mCreating Skronk Service..."
echo -e "\033[0m\033[1A"
echo ""
sudo systemctl disable skronk.service
sudo ln -sv /home/pi/skronk/skronk/skronk.service /etc/systemd/system/skronk.service
sudo systemctl enable skronk.service
sudo systemctl start skronk.service
echo ""

#-------------------------------------------------------------------------------
# install complete
#-------------------------------------------------------------------------------
echo -e "\033[1mSkronk Install Complete"
echo -e "\033[0m\033[1A"
echo ""
echo "Goodbye :)"
echo ""


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
