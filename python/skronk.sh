#!/bin/bash

# Join or run the skronk python script in a screen instance named skronk
# Cooper Baker (c) 2024

if sudo screen -ls skronk | grep skronk; then
    sudo screen -r skronk
else
    sudo screen -c $(dirname "$0")/SKRONK/scripts/skronk_rc -S skronk /usr/bin/python3 $(dirname "$0")/skronk.py
fi