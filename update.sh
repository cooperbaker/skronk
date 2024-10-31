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
git pull
rm -v ./skronk/install.sh
chmod -v 755 ./skronk/skronk.py
chmod -v 755 ./skronk/update.py
echo ""
echo -e "\033[1mUpdate Complete"
echo -e "\033[0m\033[1A"
echo ""
echo "Goodbye :)"
echo ""


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------