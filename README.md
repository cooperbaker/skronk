# Skronk Hat Firmware

&nbsp;
## SD Card Flashing Instructions

Download the latest Cycling 74 RNBO Raspberry Pi image\
[https://rnbo.cycling74.com/resources#raspberry-pi-images](https://rnbo.cycling74.com/resources#raspberry-pi-images)

Unzip the image

Flash to SD card using Raspberry Pi Imager\
[https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

Raspberry Pi Imager Settings:
- Raspberry Pi Device
  - Raspberry Pi 5
- Operating System
  - Use Custom
    - Enable "All Files (*)"
    - Select the .dmg you just unzipped
- Storage
  - *your SD card*
- [ NEXT ]
- Use OS customisation?
  - [ EDIT SETTINGS ]
- General
  - Set hostname
    - *your hostname*
  - Set username and password\
    ( *username* pi *is required )*
    - pi
    - *your password*
  - Configure wireless LAN
    - *your wifi name*
    - *your wifi password*
    - *your country*
    - *hidden ssid?*
  - Set locale settings
    - *your time zone*
    - *your keyboard layout*
- Services
  - Enable SSH
    - Use password authentication
- [ SAVE ]
- Would you like to apply OS customisation settings?
  - [ YES ]
  - Warning
    - [ YES ]
    - Enter password
- Write and Verify
  - Remove SD card
    - [ CONTINUE ]
    - Quit Raspberry Pi Imager

Boot with the fresh SD card

Reboot

Activity light will flash red/green, then stay green...
&nbsp;
## Skronk Installation Instructions
- SSH into the pi\
  $ ```ssh pi@skronk```( pi@*your_hostname*)
- Enter the following command\
  $ ```curl https://raw.githubusercontent.com/cooperbaker/skronk/refs/heads/main/skronk/scripts/install.sh | bash```

&nbsp;
# Notes
## Menus
- Switch 17 toggles menu visibility
- Bold numbers indicate active switches on menus\
  *For example:* **<1 2>** *indicates left / right navigation with switches* **1** *and* **2**
## Skronk RNBO Patches
[https://github.com/cooperbaker/skronk-rnbo](https://github.com/cooperbaker/skronk-rnbo)
## Skronk Pd Patches
[https://github.com/cooperbaker/skronk-rnbo](https://github.com/cooperbaker/skronk-pd)
## Skronk service
  - display status\
    $ ```sudo systemctl status skronk.service```
  - start now\
    $ ```sudo systemctl start skronk.service```
  - restart now\
    $ ```sudo systemctl restart skronk.service```
  - stop now\
    $ ```sudo systemctl stop skronk.service```
## Skronk command-line
- stop skronk service\
  $ ```sudo systemctl stop skronk.service```
- run skronk\
  $ ```cd /home/pi/skronk```\
  $ ```sudo python3 skronk.py```
- stop skronk\
  $ ```ctrl-c```
## Alsa audio system
- list all devices\
  $ ```aplay -l```
- list device names only\
  $ ```aplay -l | awk -F \: '/,/{print $2}' | awk '{print $1}' | uniq```
- termainal-based mixer\
  $ ```alsamixer```
