#!/bin/bash

# RNBO Normal Use Setup for Raspberry PI OS Lite
# Cooper Baker - (c)2024
# https://github.com/Cycling74/rnbo.oscquery.runner/blob/main/README-rpi.md

RNBO_VERSION="1.2.2"

# sudo su
# run this script as root from the same directory as the script

# Normal use
rm -f /etc/xdg/autostart/piwiz.desktop
apt-key add apt-cycling74-pubkey.asc
mv cycling74.list /etc/apt/sources.list.d/
apt -y remove pulseaudio libpulse0 pulseaudio-utils libpulsedsp
apt update
apt -y install jackd2 ccache cpufrequtils
echo "GOVERNOR=\"performance\"" > /etc/default/cpufrequtils
apt -y upgrade
apt-get -y autoremove
dpkg-reconfigure jackd2
echo snd-dummy >> /etc/modules
apt-get install -y --allow-change-held-packages --allow-downgrades --install-recommends --install-suggests rnbooscquery="$RNBO_VERSION"
apt-mark hold rnbooscquery

rm apt-cycling74-pubkey.asc
read -rsp $'Press any key to reboot...\n' -n1 key
reboot now
