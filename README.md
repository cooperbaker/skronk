# Skronk Hat



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
    - Select the .dmg that you just unzipped
- Storage
  - *your SD card*
- [ NEXT ]
- Use OS customisation?
  - [ EDIT SETTINGS ]
- General
  - Set hostname
    - skronk *. . . or whatever hostname you want*
  - Set username and password ( *RNBO requires username* pi *)*
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
- Write and Verify
  - Remove SD card
    - [ CONTINUE ]
    - Quit Raspberry Pi Imager

Boot with the fresh SD card

Reboot

Activity light will flash red/green eventually stay green

## Installation Instructions
- SSH into the pi\
  $ ```ssh pi@skronk```( pi@*your_hostname*)
- Enter the following command\
  $ ```curl https://raw.githubusercontent.com/cooperbaker/skronk/refs/heads/main/install.sh | bash```

## Notes

### skronk systemctl service
  - display status\
    $ ```sudo systemctl status skronk.service```
  - start now\
    $ ```sudo systemctl start skronk.service```
  - restart now\
    $ ```sudo systemctl restart skronk.service```
  - stop now\
    $ ```sudo systemctl stop skronk.service```
### skronk command-line
---
- stop skronk service\
  $ ```sudo systemctl stop skronk.service```
- run skronk\
  $ ```sudo python3 /home/pi/skronk/skronk.py```
- stop skronk\
  $ ```ctrl-c```
### alsa audio system
---
- list all devices\
  ```$ aplay -l```

- list device names only\
  ```$ aplay -l | awk -F \: '/,/{print $2}' | awk '{print $1}' | uniq```

- termainal-based mixer\
  ```$ alsamixer```

