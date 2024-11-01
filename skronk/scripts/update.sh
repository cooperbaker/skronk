#!/bin/bash
#-------------------------------------------------------------------------------
# update.sh
#
# Skronk library update script
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


echo ""
echo -e "\033[1mUpdating Skronk Library"
echo -e "\033[0m\033[1A"
echo ""

echo -e "\033[1mSyncing With Github..."
echo -e "\033[0m\033[1A"
echo ""
cd ~
cd skronk
git pull
echo ""

echo -e "\033[1mSetting Permissions..."
echo -e "\033[0m\033[1A"
echo ""
cd ~
chmod -v 755 ./skronk/skronk.py
chmod -v 755 ./skronk/skronk/scripts/update.sh
chmod -v 555 ./skronk/skronk/scripts/install.sh
echo ""

echo -e "\033[1mUpdate Complete"
echo -e "\033[0m\033[1A"
echo ""
echo "Goodbye :)"
echo ""


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------