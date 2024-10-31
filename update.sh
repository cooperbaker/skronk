#!/bin/bash
#-------------------------------------------------------------------------------
# update.sh
#
# Skronk library update script
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


echo ""
echo -e "\033[1mUpdating Skronk Library..."
echo -e "\033[0m\033[1A"
echo ""
cd ~
cd skronk
git pull
chmod -v 755 skronk.py
echo ""
echo -e "\033[1mUpdate Complete"
echo -e "\033[0m\033[1A"
echo ""
echo "Goodbye :)"
echo ""


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------